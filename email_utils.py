import sendgrid

import constants


def get_email_client(api_key):
    return sendgrid.SendGridAPIClient(api_key=api_key)


def build_email_from_usernames(sender, user_infos):
    recipients = _get_recipients_from_usernames(user_infos)
    subject = _get_subject(user_infos)
    content = _get_content(user_infos)
    return _build_email(sender, recipients, subject, content)


def _build_email(sender, recipients, subject, content):
    message = sendgrid.Mail()
    message.from_email = sender
    message.to = recipients
    message.subject = subject
    message.add_content(content, 'text/html')
    return message


def _get_recipients_from_usernames(user_infos):
    return [f"{info['username']}@dimagi.com" for info in user_infos]


def _get_subject(user_infos):
    group_text = 'duo' if len(user_infos) == 2 else 'trio'
    formatted_usernames = ', '.join([info['username'] for info in user_infos])
    return f'Your code review {group_text}: {formatted_usernames}'


def _get_content(user_infos):
    troll_content = ''
    if len(user_infos) == 3:
        troll_content = constants.TROLL_COPY.format(user_infos[2]['username'],
                                                    user_infos[2]['preference'])
    return constants.COPY.format(user_infos[0]['username'],
                                 user_infos[0]['preference'],
                                 user_infos[1]['username'],
                                 user_infos[1]['preference'],
                                 troll_content)
