from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    abort,
)
from flask_login import login_required, current_user
from models import db, User, StudentBody, Conversation, Message
from sqlalchemy import or_
from datetime import datetime, timezone

messaging_bp = Blueprint("messaging", __name__)


def get_user_details(prefixed_id):
    """Helper function to get name, profile pic, and URL from a prefixed ID."""
    if prefixed_id.startswith("U_"):
        user_id = prefixed_id[2:]
        user = User.query.get(user_id)
        if user:
            pic = user.profile_pic or "default-profile.png"
            pic_url = url_for("static", filename=pic)
            return {
                "name": user.name,
                "profile_pic_url": pic_url,
                "id": user.get_id(),
                "url": url_for("profile.view_profile", user_id=user.id),
            }
    elif prefixed_id.startswith("B_"):
        body_id = int(prefixed_id[2:])
        body = StudentBody.query.get(body_id)
        if body:
            # profile.html uses a hardcoded path based on name.
            pic_url = url_for("static", filename=f"StudentBody/{body.name}.webp")
            return {
                "name": body.name,
                "profile_pic_url": pic_url,
                "id": body.get_id(),
                "url": url_for("studentbody.view_body", body_id=body.id),
            }

    # Fallback for unknown/deleted users
    return {
        "name": "Unknown User",
        "profile_pic_url": url_for("static", filename="default-profile.png"),
        "id": "",
        "url": "#",
    }


@messaging_bp.route("/messages")
@login_required
def inbox():
    my_id = current_user.get_id()

    # Find all conversations this user is part of
    conversations = (
        Conversation.query.filter(
            or_(
                Conversation.participant_one == my_id,
                Conversation.participant_two == my_id,
            )
        )
        .order_by(Conversation.last_updated.desc())
        .all()
    )

    chat_partners = []
    for conv in conversations:
        # Determine the *other* participant
        other_participant_id = (
            conv.participant_two
            if conv.participant_one == my_id
            else conv.participant_one
        )

        # Get their details
        other_user_details = get_user_details(other_participant_id)

        # Get the last message for preview
        last_message = (
            Message.query.filter_by(conversation_id=conv.id)
            .order_by(Message.timestamp.desc())
            .first()
        )

        # Check for unread messages
        unread_count = Message.query.filter_by(
            conversation_id=conv.id, receiver_id=my_id, is_read=False
        ).count()

        chat_partners.append(
            {
                "user": other_user_details,
                "last_message": last_message,
                "conversation_id": conv.id,
                "unread_count": unread_count,
            }
        )

    return render_template("messages_inbox.html", chat_partners=chat_partners)


@messaging_bp.route("/messages/<int:conversation_id>", methods=["GET", "POST"])
@login_required
def view_conversation(conversation_id):
    conv = Conversation.query.get_or_404(conversation_id)
    my_id = current_user.get_id()

    # Security check: Ensure current user is part of this conversation
    if my_id not in [conv.participant_one, conv.participant_two]:
        abort(403)  # Forbidden

    other_participant_id = (
        conv.participant_two if conv.participant_one == my_id else conv.participant_one
    )
    other_user_details = get_user_details(other_participant_id)

    if request.method == "POST":
        content = request.form.get("content")
        if content:
            # Create and save the new message
            new_msg = Message(
                conversation_id=conv.id,
                sender_id=my_id,
                receiver_id=other_participant_id,
                content=content,
                timestamp=datetime.now(timezone.utc)(),
            )
            db.session.add(new_msg)

            # Update the conversation's last_updated timestamp
            conv.last_updated = datetime.now(timezone.utc)()
            db.session.commit()

            # Redirect back to the same page to show the new message
            return redirect(
                url_for("messaging.view_conversation", conversation_id=conversation_id)
            )

    # Load all messages for this chat
    messages = (
        Message.query.filter_by(conversation_id=conversation_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    # Mark messages sent *to me* in *this* chat as read
    Message.query.filter_by(
        conversation_id=conversation_id, receiver_id=my_id, is_read=False
    ).update({"is_read": True})
    db.session.commit()

    return render_template(
        "conversation.html",
        messages=messages,
        other_user_details=other_user_details,
        conversation_id=conv.id,
    )


@messaging_bp.route("/api/send_message", methods=["POST"])
@login_required
def api_send_message():
    data = request.json
    receiver_id = data.get(
        "receiver_id"
    )  # This is the prefixed ID ("U_..." or "B_...")
    content = data.get("content")
    sender_id = current_user.get_id()

    if not receiver_id or not content:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    if receiver_id == sender_id:
        return jsonify({"status": "error", "message": "Cannot message yourself"}), 400

    # Find or create the conversation
    # We sort participants to ensure (userA, userB) is the same as (userB, userA)
    participants = sorted([sender_id, receiver_id])
    p1 = participants[0]
    p2 = participants[1]

    conv = Conversation.query.filter_by(participant_one=p1, participant_two=p2).first()

    if not conv:
        conv = Conversation(
            participant_one=p1,
            participant_two=p2,
            last_updated=datetime.now(timezone.utc)(),
        )
        db.session.add(conv)
        # We need the conversation ID, so we commit here
        db.session.commit()

    # Create and save the new message
    new_msg = Message(
        conversation_id=conv.id,
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.now(timezone.utc)(),
    )
    db.session.add(new_msg)

    # Update the conversation's last_updated timestamp
    conv.last_updated = datetime.now(timezone.utc)()

    db.session.commit()

    return jsonify(
        {"status": "success", "message": "Message sent", "conversation_id": conv.id}
    )
