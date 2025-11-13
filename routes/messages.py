from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, StudentBody, Conversation, Message
from sqlalchemy import or_

messages_bp = Blueprint('messages', __name__)

def get_user_by_generic_id(user_id):
    """Fetches a user (student or body) by their prefixed ID."""
    if user_id.startswith("U_"):
        return User.query.get(user_id[2:])
    elif user_id.startswith("B_"):
        return StudentBody.query.get(int(user_id[2:]))
    return None

@messages_bp.route('/messages')
@login_required
def list_conversations():
    user_id = current_user.get_id()

    conversations = db.session.query(Conversation).filter(
        or_(Conversation.user_one_id == user_id, Conversation.user_two_id == user_id)
    ).order_by(Conversation.last_message_time.desc()).all()

    chat_partners = []
    for conv in conversations:
        partner_id = conv.user_two_id if conv.user_one_id == user_id else conv.user_one_id
        partner = get_user_by_generic_id(partner_id)
        if partner:
            last_message = Message.query.filter_by(conversation_id=conv.id).order_by(Message.timestamp.desc()).first()
            chat_partners.append({
                'partner': partner,
                'last_message': last_message.content if last_message else "No messages yet.",
                'timestamp': last_message.timestamp if last_message else conv.last_message_time,
                'conversation_id': conv.id
            })

    return render_template('messages.html', chat_partners=chat_partners)

@messages_bp.route('/chat/<conversation_id>', methods=['GET', 'POST'])
@login_required
def chat(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    user_id = current_user.get_id()

    # Security check: ensure current user is part of this conversation
    if user_id not in [conversation.user_one_id, conversation.user_two_id]:
        flash('You are not authorized to view this conversation.', 'danger')
        return redirect(url_for('messages.list_conversations'))

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            receiver_id = conversation.user_two_id if conversation.user_one_id == user_id else conversation.user_one_id

            new_message = Message(
                conversation_id=conversation.id,
                sender_id=user_id,
                receiver_id=receiver_id,
                content=content
            )

            # Update conversation's last message time
            conversation.last_message_time = new_message.timestamp

            db.session.add(new_message)
            db.session.commit()

            return redirect(url_for('messages.chat', conversation_id=conversation.id))

    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.timestamp.asc()).all()

    partner_id = conversation.user_two_id if conversation.user_one_id == user_id else conversation.user_one_id
    partner = get_user_by_generic_id(partner_id)

    return render_template('chat.html', messages=messages, conversation_id=conversation.id, partner=partner)

@messages_bp.route('/start_chat/<receiver_id>')
@login_required
def start_chat(receiver_id):
    sender_id = current_user.get_id()

    # Ensure users are not trying to chat with themselves
    if sender_id == receiver_id:
        flash("You cannot start a conversation with yourself.", "warning")
        return redirect(request.referrer or url_for('dashboard.dashboard'))

    # Sort IDs to ensure the pair is always stored in the same order
    user_ids = sorted([sender_id, receiver_id])
    user_one_id, user_two_id = user_ids[0], user_ids[1]

    conversation = Conversation.query.filter_by(
        user_one_id=user_one_id,
        user_two_id=user_two_id
    ).first()

    if not conversation:
        conversation = Conversation(
            user_one_id=user_one_id,
            user_two_id=user_two_id
        )
        db.session.add(conversation)
        db.session.commit()

    return redirect(url_for('messages.chat', conversation_id=conversation.id))
