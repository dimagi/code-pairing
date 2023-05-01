Code Pairs
====
This script allows you to assign new code pairs by running this command:
```
python runner.py
```

### Configuration Setup
The application needs the following environment variables set to work properly:
- SENDGRID_API_KEY (Valid API key to make requests via SendGrid)
- FROM_EMAIL (Email address to send emails from)

### Tests
Run:
```
nosetests
```

### Etiquette
- If you know you will be offline for an entire 2 week rotation, please submit a
PR to remove yourself from the `config.yml` file.
