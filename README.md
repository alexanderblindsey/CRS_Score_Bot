# CRS_Score_Bot
#### V1.0
_This is a work in progress. V2.0 will do a lot more things._

V1.0: Released January 2, 2021

## Purpose

Immigrants applying for permanent residency (PR) in Canada have a Comprehensive Ranking System (CRS) score,\
where you get more points depending on your age, education, languages, work experience, etc. Immigration\
Canada (IRCC) pools together applicants, and every two weeks, they draw the top x number of applicants\
from the pool and invite them to apply for PR. As such, the minimum CRS score needed to recieve an\ 
invitation to apply (ITA) from IRCC changes regularly as the applicant pool changes.

As such, immigrants in this pool are continuously curious as to what the most recent minimum CRS score was\
to recieve an ITA. I noticed that many Redditors on the [r/ImmigrationCanada subreddit](https://www.reddit.com/r/ImmigrationCanada) were continuously\
asking what the required score is. 

If a redditor comments "!CRS" in the subreddit, the CRS_Score_Bot replies with details of the most recent draw.

## Description

The bot, which is hosted on Google Cloud, scrapes this [IRCC website](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry/submit-profile/rounds-invitations.html) to collect data on the most recent\
express entry draw. The continuously scans r/CanadaImmigration comments and searches for "!CRS", at which point\
it replies to the comment with this data.

## Feedback

If you have any feedback, questions, or concerns, email me at [alexander.lindsey96@gmail.com](alexander.lindsey96@gmail.com).  