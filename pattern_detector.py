
def detect_patterns(text):

    text = text.lower()

    patterns = {
        "Nagging": [
            "remind me again",
            "don't miss out",
            "do not miss out",
            "subscribe now",
            "limited time offer",
            "last chance",
            "special offer"
        ],

        "Obstruction": [
            "contact support to cancel",
            "cancellation is unavailable",
            "call us to unsubscribe",
            "difficult to cancel",
            "cancel subscription",
            "cancellation process"
        ],

        "Sneaking": [
            "additional charges",
            "hidden fees",
            "extra fees apply",
            "unexpected charges",
            "shipping charges apply",
            "added charges"
        ],

        "Interface Interference": [
            "recommended option",
            "best value",
            "preselected",
            "most popular",
            "default selection",
            "recommended plan"
        ],

        "Forced Action": [
            "sign up to continue",
            "create an account to proceed",
            "login required to continue",
            "register to continue",
            "subscribe to continue",
            "sign in to continue"
        ]
    }

    detected = []

    for category, keywords in patterns.items():

        for keyword in keywords:

            if keyword in text:

                detected.append({
                    "pattern": category,
                    "evidence": keyword
                })

    return detected
