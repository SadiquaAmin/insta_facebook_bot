from instabot import Bot


class InstaBotTest:
    def test_upload_story(self):
        # Initialize a bot instance
        bot = Bot()

        # Login to your Instagram account
        bot.login(username="anna_jian_sf", password="hackathon123")

        # Upload a story
        bot.upload_story_photo("ali.jpg", caption="Your story caption")
        bot.publi

        # Logout from your Instagram account
        bot.logout()

if __name__=="__main__":
    InstaBotTest().test_upload_story()