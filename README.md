Code Pairs
====
This script allows you to assign new code pairs by running this command:
```
python runner.py
```

### Setup on Jenkins

1. The code pairing directory should live in `/var/lib/code-pairing`.
2. Run `pip install -r requirements.txt`
3. Copy cron command from the `two_week_cron_job` and place in crontab

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

- If you are gone for a week or two, please submit a PR to remove yourself from the `config.yml` file.
- Feel free to change whether you belong in the `enchantress` or `hobbit` camp. `hobbits` are generally newer
  while `enchantresses` are generally more experienced. Try and keep the two lists roughly equal. The script 
      will handle odd numbers or uneven groups.
- Once you get your partner, you should ping them on each PR you make. There should be low bar to bring in
  someone else who has more context on the PR.
