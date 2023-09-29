# Daily Hoyo Checkin

Aka a bot that checks in daily on a certain anime waifu/husbando collector website.

# ltoken and ltuid Cookie Extraction Guide

This guide will walk you through the process of extracting the `ltoken` and `ltuid` values from the cookies on the daily check-in page using Google Chrome's developer tools.

## Prerequisites

Google Chrome browser installed on your computer.

## Steps

1. Open the daily check-in page
   Open your Google Chrome browser.
   Navigate to the website and log in to your account if you haven't already.
2. Open developer tools and find the cookies tab
   Once you are on the website and logged in, press F12 or right-click on any element on the page and select "Inspect" from the context menu. This will open the Chrome Developer Tools panel. In the Developer Tools panel, you will see several tabs. Click on the "Application" tab. This tab contains information about the website's cookies, among other things. In the left sidebar of the "Application" tab, expand the "Cookies" section. You will see various options like "Cookies," "Local Storage," and "Session Storage."
   Under the "Cookies" section, you should see a list of domains. Look for and click on the one related to the website.
3. Find ltoken and ltuid cookies
   In the list of cookies for the game's domain, you should be able to find the `ltoken` and `ltuid` cookies.
4. Copy the values
   To extract the ltoken and ltuid values, simply double-click on the respective cookie values, and it will allow you to copy them to your clipboard.

That's it! You have successfully extracted the ltoken and ltuid values from the website's cookies using Google Chrome's developer tools.

**Important Note:** Treat these values with care and do not share them with others, as they are sensitive authentication tokens and user identifiers.
