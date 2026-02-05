# spendlocal — iOS Shortcut Setup

This guide explains how to create an iOS Shortcut that logs expenses to your spendlocal server.

## Quick Start: Import Template

**[Download the Shortcut](https://www.icloud.com/shortcuts/aa76f6b0432a4a67bd8f90920a1c3c3c)**

After importing:
1. Open the shortcut in edit mode
2. Find the "Get Contents of URL" action
3. Replace `YOUR_SERVER_IP` with your Tailscale IP (e.g., `100.x.x.x`)
4. Done

## Manual Setup

If you prefer to build it yourself, follow the steps below.

## Prerequisites

- Tailscale installed on both your iPhone and server
- Server running and accessible via Tailscale IP (e.g., `100.x.x.x`)

## Create the Shortcut

1. Open **Shortcuts** app on iPhone
2. Tap **+** to create new shortcut
3. Add these actions in order:

### Action 1: Ask for Input (Title)
- **Action:** Ask for Input
- **Prompt:** "What was it?"
- **Input Type:** Text
- **Save to variable:** `title`

### Action 2: Ask for Input (Amount)
- **Action:** Ask for Input
- **Prompt:** "How much?"
- **Input Type:** Number
- **Save to variable:** `amount`

### Action 3: Choose from Menu (Account)
- **Action:** Choose from Menu
- **Prompt:** "Payment method"
- **Options:** Card, Cash
- **Save to variable:** `account`

### Action 4: Date (Current)
- **Action:** Date
- **Use:** Current Date
- **Format:** Custom → `yyyy-MM-dd`
- **Save to variable:** `date`

### Action 5: Get Contents of URL
- **Action:** Get Contents of URL
- **URL:** `http://YOUR_TAILSCALE_IP:5000/add`
- **Method:** POST
- **Headers:**
  - `Content-Type`: `application/json`
- **Request Body:** JSON
  ```json
  {
    "title": title,
    "amount": amount,
    "account": account,
    "date": date
  }
  ```

### Action 6: Show Notification (Optional)
- **Action:** Show Notification
- **Title:** "Expense logged"
- **Body:** `title` - €`amount`

## Apple Wallet Automation (Optional)

To auto-trigger when you pay:

1. Go to **Settings → Shortcuts → Automation**
2. Tap **+** → **Create Personal Automation**
3. Scroll down → **Transaction** (under Apple Wallet)
4. Choose: "When I tap any card"
5. Add action: **Run Shortcut** → select your expense shortcut
6. Disable "Ask Before Running" for seamless logging

Now every time you pay with Apple Wallet, you'll be prompted to log the expense.

## Testing

Test the shortcut manually first:

```bash
# From your server, test the endpoint
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "amount": 1.00, "account": "Card", "date": "2026-02-05"}'
```

## Troubleshooting

**Shortcut fails silently:**
- Check Tailscale is connected on iPhone
- Verify server IP hasn't changed
- Check server is running: `curl http://YOUR_IP:5000/health`

**"Could not connect to server":**
- Tailscale might not be active
- Server might be down
- Firewall might be blocking port 5000

**Wrong data appearing:**
- Check date format matches `yyyy-MM-dd`
- Verify account is exactly "Card" or "Cash" (case-sensitive)
