
from pattern_detector import detect_patterns

test_cases = [
    "Don't miss out! Limited time offer.",
    "Contact support to cancel your subscription.",
    "Additional charges apply.",
    "Recommended option: Premium Membership.",
    "Sign up to continue shopping.",
    "Welcome to our website. Enjoy shopping!"
]

for i, text in enumerate(test_cases, 1):
    print(f"\nTest {i}: {text}")
    print("Detected:", detect_patterns(text))
