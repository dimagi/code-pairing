import sendgrid

import constants


def get_email_client(api_key):
    return sendgrid.SendGridAPIClient(api_key=api_key)


def build_email_from_usernames(sender, usernames):
    recipients = _get_recipients_from_usernames(usernames)
    subject = _get_subject(usernames)
    content = _get_content(usernames)
    return _build_email(sender, recipients, subject, content)


def _build_email(sender, recipients, subject, content):
    message = sendgrid.Mail()
    message.from_email = sender
    message.to = recipients
    message.subject = subject
    message.add_content(content, 'text/html')
    return message


def _get_recipients_from_usernames(usernames):
    return [f"{username}@dimagi.com" for username in usernames]


def _get_subject(usernames):
    group_text = 'duo' if len(usernames) == 2 else 'trio'
    formatted_usernames = ', '.join(usernames)
    return f'Your code review {group_text}: {formatted_usernames}'


def _get_content(usernames):
    troll_content = ''
    if len(usernames) == 3:
        troll_content = constants.TROLL_COPY.format(usernames[2])
    return constants.COPY.format(usernames[0], usernames[1], troll_content)
