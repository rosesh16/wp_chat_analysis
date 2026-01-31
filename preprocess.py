import re
import pandas as pd

def preprocess(data):
  pattern = r'\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s*(?:am|pm)\s-\s'

  messages = [m for m in re.split(pattern, data) if m.strip()]

  data = data.replace('\u202f', ' ')

  dates = re.findall(pattern,data)

  df = pd.DataFrame({'user_message':messages, 'message_date':dates})
  #Convert message_date type
  df['message_date'] = (
    df['message_date']
    .str.replace('\u202f', ' ', regex=False)
    .str.replace(r'\s-\s$', '', regex=True)
)

  df['message_date'] = pd.to_datetime(df['message_date'],format='%d/%m/%Y, %I:%M %p')

  df.rename(columns={'message_date':'date'},inplace=True)


  users = []
  messages_list = []

  for msg in df['user_message']:
    entry = re.split(r'^([^:]+):\s', msg, maxsplit=1)

    if len(entry) > 1:
        users.append(entry[1])
        messages_list.append(entry[2])
    else:
        users.append('group_notification')
        messages_list.append(entry[0])

  df['user'] = users
  df['message'] = messages_list
  df.drop(columns=['user_message'], inplace=True)

  df['year'] = df['date'].dt.year
  df['month'] = df['date'].dt.month_name()
  df['month_num'] = df['date'].dt.month
  df['only_date'] = df['date'].dt.date
  df['day'] = df['date'].dt.day
  df['day_name'] = df['date'].dt.day_name()
  df['hour'] = df['date'].dt.hour
  df['minute'] = df['date'].dt.minute


  period = []
  for hour in df[['day_name','hour']]['hour']:
    if hour == 23:
      period.append(str(hour) + "-" + str('00'))
    elif hour == 0:
      period.append(str('00') + "-" + str(hour+1))
    else:
      period.append(str(hour) + "-" + str(hour+1))   

  df['period'] = period    

  return df

