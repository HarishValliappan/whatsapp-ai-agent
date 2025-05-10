from pywa import WhatsApp, filters, types
from fastapi import FastAPI

fastapi_app = FastAPI() # FastAPI server

# Create a WhatsApp client
wa = WhatsApp(
    phone_id=639451852586281,
    token="EAARUh0IXTHQBO0NrY6isN2EGKqLUeYClcUbX0eAeJHTC3rnMilRKuT54lFCEGRGg4QeMAtfZCZBklXAKqmytOHIEUw4YHneffq8NZAEBc8X4438nqRpt7PZAb2WsPEd7yfPlxLaWfoV8KWrXqcp8fMfDLxUh53rup2R3VwqUbS1xGDOHjJRXRLcOxrY4i6ry3GqCsLscOywZBLJlxKtT3BrAZD",
    server=fastapi_app, # the server to listen to incoming updates
    callback_url="https://yourdomain.com/",  # the public URL of your server
    verify_token="xyz123", # some random string to verify the webhook
    app_id=123456, # your app id
    app_secret="*******" # your app secret
)

# Register callback to handle incoming messages
@wa.on_message(filters.matches("Hello", "Hi")) # Filter to match text messages that contain "Hello" or "Hi"
def hello(client: WhatsApp, msg: types.Message):
    msg.react("👋") # React to the message with a wave emoji
    msg.reply_text( # Short reply to the message
        text=f"Hello {msg.from_user.name}!", # Greet the user
        buttons=[ # Add buttons to the reply
            types.Button(
                title="About me",
                callback_data="about_me" # Callback data to identify the click
            )
        ]
    )
    # Use the `wait_for_reply` listener to wait for a reply from the user
    age = msg.reply(text="What's your age?").wait_for_reply(filters=filters.text).text
    msg.reply_text(f"Your age is {age}.")

# Register another callback to handle incoming button clicks
@wa.on_callback_button(filters.matches("about_me")) # Filter to match the button click
def click_me(client: WhatsApp, clb: types.CallbackButton):
    clb.reply_text(f"Hello {clb.from_user.name}, I am a WhatsApp bot built with PyWa!") # Reply to the button click