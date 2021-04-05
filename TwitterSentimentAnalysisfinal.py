  #!/usr/bin/env python
  # coding: utf-8

  # In[1]:


  # 1. Import Libraries

def mainproject(topic):
  import pandas as pd
  import numpy as np
  import matplotlib.pyplot as plt
  import seaborn as sns
  import tweepy
  from tweepy import OAuthHandler


  # In[2]:


  # 2.Set Connecion

  #Get from developers.twitter.com/App->Setting->keys&tokens
  #Just assign the credentials

  consumer_key = "5Y7DWu6MADOLdhs0EOEYGdthn"
  consumer_secret = "HhTWe40oax3jAbkTOvPMzCQ0cEhZVZqFwi3s2VoMNjwG0aTTTf"
  access_token = "378151731-ohoLskEKuIHIaLbsmLqEiaQvTUQ0NwgffCQkqajA"
  access_token_secret = "GDYOeY9vsg1UtkHN9VL9bZthNtNdxlIZqFIL1VuPeQcaI"



  # Use the above credentials to authenticate the API.

  auth = tweepy.OAuthHandler( consumer_key , consumer_secret )
  auth.set_access_token( access_token , access_token_secret )
  api = tweepy.API(auth)


  # In[3]:


  # 3.To get the tweets in a Proper format, first lets create a Dataframe to store the extracted data.

  df = pd.DataFrame(columns=["Date","User","IsVerified","Tweet","Likes","RT",'User_location'])
  #print(df)


  # In[4]:


  # We will use api as api.search inside this tweepy cursor.


  # In[7]:


  # 4.Write a Function to extract tweets:

  # We will Use **tweepy.cursor()** because we want to extract a larger number of tweets i.e over 100,500 etc


  def get_tweets(Topic,Count):    
      i=0
      for tweet in tweepy.Cursor(api.search, q=Topic,count=100, lang="en",exclude='retweets').items():
          print(i, end='\r')
          df.loc[i,"Date"] = tweet.created_at
          df.loc[i,"User"] = tweet.user.name
          df.loc[i,"IsVerified"] = tweet.user.verified
          df.loc[i,"Tweet"] = tweet.text
          df.loc[i,"Likes"] = tweet.favorite_count      
          df.loc[i,"RT"] = tweet.retweet_count
          df.loc[i,"User_location"] = tweet.user.location
          #df.to_csv("TweetDataset.csv",index=False)
          df.to_excel('{}.xlsx'.format("TweetDataset"),index=False)   ## Save as Excel
          i=i+1
          if i>Count:
              break
          else:
              pass
          


  # In[8]:


  # Call the function to extract the data. pass the topic and filename you want the data to be stored in.
  Topic= [topic]
  get_tweets(Topic , Count=100)


  # In[9]:


 # df.head(8)


  # # Analyze the tweets

  # In[10]:


  # Function to Clean the Tweet.

  import re
  def clean_tweet(tweet):
      return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|([RT])', ' ', str(tweet).lower()).split())

  # We only want the Text so :

  # (@[A-Za-z0-9]+)   : Delete Anything like @hello @Letsupgrade etc
  # ([^0-9A-Za-z \t]) : Delete everything other than text,number,space,tabspace
  # (\w+:\/\/\S+)     : Delete https://
  # ([RT]) : Remove "RT" from the tweet


  # In[11]:


  # Funciton to analyze Sentiment

  from textblob import TextBlob
  def analyze_sentiment(tweet):
      analysis = TextBlob(tweet)
      if analysis.sentiment.polarity > 0:
          return 'Positive'
      elif analysis.sentiment.polarity == 0:
          return 'Neutral'
      else:
          return 'Negative'


  # In[12]:


  #Function to Pre-process data for Worlcloud:here we are removing the words present in Topic from the Corpus so they dont come in WordCloud.
  # Ex : Topic is "Arsenal vs United", we want to remove "Arsenal" "vs" "United" from the WordCloud.

  def prepCloud(Topic_text,Topic):
      Topic = str(Topic).lower()
      Topic=' '.join(re.sub('([^0-9A-Za-z \t])', ' ', Topic).split())
      Topic = re.split("\s+",str(Topic))
      stopwords = set(STOPWORDS)
      stopwords.update(Topic) ### Add our topic in Stopwords, so it doesnt appear in wordClous
      ###
      text_new = " ".join([txt for txt in Topic_text.split() if txt not in stopwords])
      return text_new


  # In[13]:


  # Call function to get Clean tweets

  df['clean_tweet'] = df['Tweet'].apply(lambda x : clean_tweet(x))
  #df.head(5)


  # In[14]:


  # Call function to get the Sentiments

  df["Sentiment"] = df["Tweet"].apply(lambda x : analyze_sentiment(x))
  #df.head(5)


  # In[15]:


  # Check Summary of Random Record
  n = 15
  print("Original tweet:\n",df['Tweet'][n])
  print()
  print("Clean tweet:\n",df['clean_tweet'][n])
  print()
  print("Sentiment of the tweet:\n",df['Sentiment'][n])


  # In[16]:


  # Overall Summ



  # In[17]:


  # df["Sentiment"].value_counts()


  # In[18]:


  #sns.countplot(df["Sentiment"],facecolor=(0, 0, 0, 0),linewidth=5,edgecolor=sns.color_palette("dark", 3))
  #sns.countplot(df["Sentiment"])
  #plt.title("Summary of Counts for Total tweets")


  # In[ ]:





  # In[19]:


  # Piechart 
  #string, used to label the wedges with their numeric value. The label will be placed inside the wedge. The format string will be fmt%pct.


  # explode = (0.1, 0.0, 0.1)
 # plt.pie(d,shadow=True,explode=explode,labels=["Positive","Negative","Neutral"],autopct='%1.2f%%');
#

  # In[20]:


  #sns.countplot(df["Sentiment"],hue=df.IsVerified)
  #plt.title("Summary of Counts for Total tweets,Distributed by if the User has a verified Account or not")


  # # Generate WordCloud

  # In[21]:


  from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


  # In[22]:


  # Start with one review:

  text = df.clean_tweet[2]

  # # Create and generate a word cloud image:
  # wordcloud = WordCloud(max_words=10).generate(text)

  # # Display the generated image:
  # plt.imshow(wordcloud, interpolation='bilinear')
  # plt.axis("off")
  # plt.show()


  # - **WordCloud for whole data(Topic not included in WordCloud)**

  # In[23]:


  # Combine all reviews into one big text and create a Cloud to see which Words are most common in these Tweets.

  #text = " ".join(review for review in df.clean_tweet)
  #print ("There are {} words in the combination of all review.".format(len(text)))


  # Create stopword list:
  #stopwords = set(STOPWORDS)
  #stopwords.update(["drink", "now", "wine", "flavor", "flavors"])  #To add any custom StopWords

  #text_newALL = prepCloud(text,Topic)


  # # Generate a word cloud image
  # wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_newALL)

  # Display the generated image:
  # the matplotlib way:


  # plt.figure(figsize=(12,8))
  # plt.imshow(wordcloud, interpolation='bilinear')
  # plt.title("The most frequently used words when searching for {}".format(Topic),)
  # plt.axis("off")
  # plt.show()


  # ## NEW

  # - **Wordcloud for Positive tweets only (Topic not included in WordCloud)**

  # In[24]:


  # Combine POSITIVE reviews into one big text and create a Cloud to see which Words are most common in these Tweets.

  #text_positive = " ".join(review for review in df[df["Sentiment"]=="Positive"].clean_tweet)
  #print ("There are {} words in the combination of all review.".format(len(text)))


  # Create stopword list:
  #stopwords = set(STOPWORDS)
  #stopwords.update(["and", "now", "wine", "flavor", "flavors"])  #To add any custom StopWords
  #text_positive=" ".join([word for word in text_positive.split() if word not in stopwords])

  #text_new_positive = prepCloud(text_positive,Topic)

  #stopwords.update(["drink", "now", "wine", "flavor", "flavors"])  #To add any custom StopWords

  # Generate a word cloud image
  # wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_new_positive)

  # Display the generated image:
  # the matplotlib way:


  # plt.figure(figsize=(12,8))
  # plt.imshow(wordcloud, interpolation='bilinear')
  # plt.title("The most frequently used words when searching for {}".format(Topic))
  # plt.axis("off")
  # plt.show()


  # - **Wordcloud for Negative tweets only  (Topic not included in WordCloud)**

  # In[25]:


  # Combine Negative reviews into one big text and create a Cloud to see which Words are most common in these Tweets.

  #text_negative = " ".join(review for review in df[df["Sentiment"]=="Negative"].clean_tweet)
  
  #print ("There are {} words in the combination of all review.".format(len(text)))


  # Create stopword list:
  #stopwords = set(STOPWORDS)
  #stopwords.update(["and", "now", "wine", "flavor", "flavors"])  #To add any custom StopWords

  #text_negative=" ".join([word for word in text_negative.split() if word not in stopwords])
  #text_new_negative = prepCloud(text_negative,Topic)

  # # Generate a word cloud image
  # wordcloud = WordCloud(stopwords=stopwords,max_words=800,max_font_size=70).generate(text_new_negative)

  # Display the generated image:
  # the matplotlib way:


  # plt.figure(figsize=(12,8))
  # plt.imshow(wordcloud, interpolation='bilinear')
  # plt.title("The most frequently used words when searching for {}".format(Topic))
  # plt.axis("off")
  # plt.show()


  # # Movie Recommendation System (part 2)
  # 
  # 

  # In[26]:


  movies = pd.read_csv("IMDb movies.csv")
  #movies.head()


  # In[27]:


  movies.describe()
  list(movies.columns)


  # In[28]:


  movies = movies.drop(columns = ['reviews_from_critics','avg_vote',
   'votes',  'date_published',
   'budget',
   'usa_gross_income',
   'worlwide_gross_income',
   'metascore',
   'reviews_from_users','original_title','language', 'production_company', 'director','writer', 'country'])


  # In[29]:


  survey = pd.read_csv("Online Movies and TV Shows.csv")
  survey.head()


  # In[30]:


  survey.isnull().sum()


  # In[31]:


  fav = survey['FavGene'].unique()
  fav


  # In[32]:


  happy = survey[' happy'].unique()


  # In[33]:


  sad = survey['Sad'].unique()


  # In[34]:


  len(happy), len(sad)


  # In[35]:


  length = survey['movie-length'].unique()


  # In[36]:


  x = np.where(movies['genre'] == 'Romance')
  index = [0,   119,   227,   279,   396,  1031,  3006,  3909,  4524,
          9226,  9996, 10238, 13302, 14358, 16694, 17691, 17765, 18115,
         18523, 21103, 21139, 23433, 25480, 25948, 26070, 26168, 27083,
         28617, 28645, 30130, 30286, 31650, 31657, 32746, 33126, 33321,
         34006, 34513, 34848, 35050, 35125, 35329, 35407, 35663, 36501,
         36535, 36645, 36676, 36786, 36887, 37037, 37060, 37157, 37205,
         37307, 37771, 37835, 37873, 38209, 38366, 38557, 38930, 38931,
         38937, 38948, 38981, 38997, 39124, 39453, 40039, 40102, 40146,
         40152, 40308, 40402, 40410, 40620, 40989, 41156, 41632, 41655,
         41844, 42341, 42347, 42527, 42858, 42861, 42955, 42972, 43092,
         43125, 43255, 44136, 44244, 44340, 44761, 44816, 44843, 44910,
         45385, 45410, 45423, 45474, 45504, 45516, 45522, 45578, 45676,
         45806, 46094, 46140, 46330, 46400, 46402, 46490, 46550, 46611,
         46934, 47101, 47368, 47375, 47403, 47413, 47488, 47551, 47555,
         47639, 47934, 47940, 48017, 48174, 48406, 48479, 48686, 48695,
         48849, 48855, 48856, 48960, 49147, 49366, 49650, 49655, 49742,
         50138, 50222, 50268, 50411, 50503, 50669, 50675, 50848, 51002,
         51030, 51133, 51146, 51369, 51498, 51553, 51874, 51918, 52190,
         52206, 52210, 52213, 52519, 52560, 52751, 52822, 52938, 53007,
         53144, 53194, 53243, 53423, 53494, 53501, 53606, 53775, 53908,
         53941, 53970, 53981, 54081, 54160, 54174, 54370, 54455, 54532,
         54712, 54939, 55292, 55388, 55459, 55504, 55592, 55736, 55782,
         56011, 56064, 56136, 56249, 56518, 56556, 56597, 57017, 57368,
         57377, 57388, 57630, 57631, 57725, 58004, 58027, 58104, 58184,
         58295, 58477, 58517, 58751, 58791, 59075, 59292, 59326, 59372,
         59538, 59569, 59574, 59618, 59623, 59764, 59820, 59856, 59862,
         59882, 59996, 60032, 60156, 60725, 61499, 61502, 61634, 61689,
         61823, 61842, 61844, 61866, 61910, 61971, 62194, 62408, 62589,
         62667, 62722, 62903, 63360, 63742, 63983, 64129, 64141, 64172,
         64426, 64676, 64677, 64767, 65001, 65197, 65223, 65710, 65970,
         66194, 66230, 66356, 66392, 66473, 66518, 66757, 66805, 66831,
         66832, 67233, 67381, 67544, 67962, 68077, 68205, 68265, 68351,
         68385, 68422, 68493, 68520, 68544, 68881, 68950, 69351, 69454,
         69513, 69631, 69860, 69871, 69929, 70167, 70184, 70186, 70361,
         70423, 70509, 70535, 70588, 70877, 71153, 71154, 71334, 71380,
         71489, 71773, 72432, 72520, 72599, 72622, 72656, 72684, 72761,
         72970, 73153, 73348, 73574, 73681, 73705, 73745, 73770, 74011,
         74183, 74218, 74283, 74336, 74409, 74546, 74748, 74802, 75004,
         75124, 75187, 75190, 75338, 75546, 75637, 75837, 75882, 75896,
         75943, 76039, 76055, 76097, 76231, 76315, 76427, 76583, 76680,
         76764, 76987, 77020, 77229, 77292, 77509, 77582, 77787, 78051,
         78379, 78505, 78510, 78891, 78924, 79029, 79106, 79132, 79155,
         79166, 79189, 79389, 79639, 79841, 80071, 80106, 80156, 80173,
         80233, 80404, 80545, 80964, 81020, 81032, 81081, 81144, 81172,
         81417, 81604, 81863, 82118, 82133, 82241, 82629, 82688, 82746,
         82878, 82932, 82936, 83065, 83191, 83265, 83266, 83293, 83456,
         83599, 83603, 83650, 83750, 83921, 83951, 84012, 84113, 84463,
         84483, 84516, 84531, 84573, 84613, 84621, 84748, 84924, 85023,
         85113, 85137, 85280, 85570, 85665, 85714, 85797]
  romance= []
  romance.append(movies.iloc[index])
  #surveys_df[-1:]
  #surveys_df[surveys_df['species_id'].isin([listGoesHere])]
  #romance


  # In[37]:


  happy, sad


  # In[38]:


  x = list(np.where(movies['genre'] == 'Comedy'))
  pd.options.display.max_seq_items = 2000
  print(x)
  len(x[0])


  # In[39]:

####################generating indexes for comedy
  #index = []
  #n = 1
  #for n in range(7693):
      #print(x[0][n])
     # print(',')


  # In[40]:


  index = [0
  ,
  119
  ,
  227
  ,
  279
  ,
  396
  ,
  1031
  ,
  3006
  ,
  3909
  ,
  4524
  ,
  9226
  ,
  9996
  ,
  10238
  ,
  13302
  ,
  14358
  ,
  16694
  ,
  17691
  ,
  17765
  ,
  18115
  ,
  18523
  ,
  21103
  ,
  21139
  ,
  23433
  ,
  25480
  ,
  25948
  ,
  26070
  ,
  26168
  ,
  27083
  ,
  28617
  ,
  28645
  ,
  30130
  ,
  30286
  ,
  31650
  ,
  31657
  ,
  32746
  ,
  33126
  ,
  33321
  ,
  34006
  ,
  34513
  ,
  34848
  ,
  35050
  ,
  35125
  ,
  35329
  ,
  35407
  ,
  35663
  ,
  36501
  ,
  36535
  ,
  36645
  ,
  36676
  ,
  36786
  ,
  36887
  ,
  37037
  ,
  37060
  ,
  37157
  ,
  37205
  ,
  37307
  ,
  37771
  ,
  37835
  ,
  37873
  ,
  38209
  ,
  38366
  ,
  38557
  ,
  38930
  ,
  38931
  ,
  38937
  ,
  38948
  ,
  38981
  ,
  38997
  ,
  39124
  ,
  39453
  ,
  40039
  ,
  40102
  ,
  40146
  ,
  40152
  ,
  40308
  ,
  40402
  ,
  40410
  ,
  40620
  ,
  40989
  ,
  41156
  ,
  41632
  ,
  41655
  ,
  41844
  ,
  42341
  ,
  42347
  ,
  42527
  ,
  42858
  ,
  42861
  ,
  42955
  ,
  42972
  ,
  43092
  ,
  43125
  ,
  43255
  ,
  44136
  ,
  44244
  ,
  44340
  ,
  44761
  ,
  44816
  ,
  44843
  ,
  44910
  ,
  45385
  ,
  45410
  ,
  45423
  ,
  45474
  ,
  45504
  ,
  45516
  ,
  45522
  ,
  45578
  ,
  45676
  ,
  45806
  ,
  46094
  ,
  46140
  ,
  46330
  ,
  46400
  ,
  46402
  ,
  46490
  ,
  46550
  ,
  46611
  ,
  46934
  ,
  47101
  ,
  47368
  ,
  47375
  ,
  47403
  ,
  47413
  ,
  47488
  ,
  47551
  ,
  47555
  ,
  47639
  ,
  47934
  ,
  47940
  ,
  48017
  ,
  48174
  ,
  48406
  ,
  48479
  ,
  48686
  ,
  48695
  ,
  48849
  ,
  48855
  ,
  48856
  ,
  48960
  ,
  49147
  ,
  49366
  ,
  49650
  ,
  49655
  ,
  49742
  ,
  50138
  ,
  50222
  ,
  50268
  ,
  50411
  ,
  50503
  ,
  50669
  ,
  50675
  ,
  50848
  ,
  51002
  ,
  51030
  ,
  51133
  ,
  51146
  ,
  51369
  ,
  51498
  ,
  51553
  ,
  51874
  ,
  51918
  ,
  52190
  ,
  52206
  ,
  52210
  ,
  52213
  ,
  52519
  ,
  52560
  ,
  52751
  ,
  52822
  ,
  52938
  ,
  53007
  ,
  53144
  ,
  53194
  ,
  53243
  ,
  53423
  ,
  53494
  ,
  53501
  ,
  53606
  ,
  53775
  ,
  53908
  ,
  53941
  ,
  53970
  ,
  53981
  ,
  54081
  ,
  54160
  ,
  54174
  ,
  54370
  ,
  54455
  ,
  54532
  ,
  54712
  ,
  54939
  ,
  55292
  ,
  55388
  ,
  55459
  ,
  55504
  ,
  55592
  ,
  55736
  ,
  55782
  ,
  56011
  ,
  56064
  ,
  56136
  ,
  56249
  ,
  56518
  ,
  56556
  ,
  56597
  ,
  57017
  ,
  57368
  ,
  57377
  ,
  57388
  ,
  57630
  ,
  57631
  ,
  57725
  ,
  58004
  ,
  58027
  ,
  58104
  ,
  58184
  ,
  58295
  ,
  58477
  ,
  58517
  ,
  58751
  ,
  58791
  ,
  59075
  ,
  59292
  ,
  59326
  ,
  59372
  ,
  59538
  ,
  59569
  ,
  59574
  ,
  59618
  ,
  59623
  ,
  59764
  ,
  59820
  ,
  59856
  ,
  59862
  ,
  59882
  ,
  59996
  ,
  60032
  ,
  60156
  ,
  60725
  ,
  61499
  ,
  61502
  ,
  61634
  ,
  61689
  ,
  61823
  ,
  61842
  ,
  61844
  ,
  61866
  ,
  61910
  ,
  61971
  ,
  62194
  ,
  62408
  ,
  62589
  ,
  62667
  ,
  62722
  ,
  62903
  ,
  63360
  ,
  63742
  ,
  63983
  ,
  64129
  ,
  64141
  ,
  64172
  ,
  64426
  ,
  64676
  ,
  64677
  ,
  64767
  ,
  65001
  ,
  65197
  ,
  65223
  ,
  65710
  ,
  65970
  ,
  66194
  ,
  66230
  ,
  66356
  ,
  66392
  ,
  66473
  ,
  66518
  ,
  66757
  ,
  66805
  ,
  66831
  ,
  66832
  ,
  67233
  ,
  67381
  ,
  67544
  ,
  67962
  ,
  68077
  ,
  68205
  ,
  68265
  ,
  68351
  ,
  68385
  ,
  68422
  ,
  68493
  ,
  68520
  ,
  68544
  ,
  68881
  ,
  68950
  ,
  69351
  ,
  69454
  ,
  69513
  ,
  69631
  ,
  69860
  ,
  69871
  ,
  69929
  ,
  70167
  ,
  70184
  ,
  70186
  ,
  70361
  ,
  70423
  ,
  70509
  ,
  70535
  ,
  70588
  ,
  70877
  ,
  71153
  ,
  71154
  ,
  71334
  ,
  71380
  ,
  71489
  ,
  71773
  ,
  72432
  ,
  72520
  ,
  72599
  ,
  72622
  ,
  72656
  ,
  72684
  ,
  72761
  ,
  72970
  ,
  73153
  ,
  73348
  ,
  73574
  ,
  73681
  ,
  73705
  ,
  73745
  ,
  73770
  ,
  74011
  ,
  74183
  ,
  74218
  ,
  74283
  ,
  74336
  ,
  74409
  ,
  74546
  ,
  74748
  ,
  74802
  ,
  75004
  ,
  75124
  ,
  75187
  ,
  75190
  ,
  75338
  ,
  75546
  ,
  75637
  ,
  75837
  ,
  75882
  ,
  75896
  ,
  75943
  ,
  76039
  ,
  76055
  ,
  76097
  ,
  76231
  ,
  76315
  ,
  76427
  ,
  76583
  ,
  76680
  ,
  76764
  ,
  76987
  ,
  77020
  ,
  77229
  ,
  77292
  ,
  77509
  ,
  77582
  ,
  77787
  ,
  78051
  ,
  78379
  ,
  78505
  ,
  78510
  ,
  78891
  ,
  78924
  ,
  79029
  ,
  79106
  ,
  79132
  ,
  79155
  ,
  79166
  ,
  79189
  ,
  79389
  ,
  79639
  ,
  79841
  ,
  80071
  ,
  80106
  ,
  80156
  ,
  80173
  ,
  80233
  ,
  80404
  ,
  80545
  ,
  80964
  ,
  81020
  ,
  81032
  ,
  81081
  ,
  81144
  ,
  81172
  ,
  81417
  ,
  81604
  ,
  81863
  ,
  82118
  ,
  82133
  ,
  82241
  ,
  82629
  ,
  82688
  ,
  82746
  ,
  82878
  ,
  82932
  ,
  82936
  ,
  83065
  ,
  83191
  ,
  83265
  ,
  83266
  ,
  83293
  ,
  83456
  ,
  83599
  ,
  83603
  ,
  83650
  ,
  83750
  ,
  83921
  ,
  83951
  ,
  84012
  ,
  84113
  ,
  84463
  ,
  84483
  ,
  84516
  ,
  84531
  ,
  84573
  ,
  84613
  ,
  84621
  ,
  84748
  ,
  84924
  ,
  85023
  ,
  85113
  ,
  85137
  ,
  85280
  ,
  85570
  ,
  85665
  ,
  85714
  ,
  85797]


  # In[41]:


  comedy= []
  comedy.append(movies.iloc[index])
 # comedy


  # In[42]:


  x = np.where(movies['genre'] == 'Thriller')

  print(x)
  index = x
  thriller= []
  thriller.append(movies.iloc[index])


  # In[43]:


  x = np.where(movies['genre'] == 'Action')

  print(x)
  index = x
  action= []
  action.append(movies.iloc[index])
  #print(action)


  # In[44]:


  x = np.where(movies['genre'] == 'Mystery')

  print(x)
  index = x
  mystery= []
  mystery.append(movies.iloc[index])
  #print(mystery)


  # In[45]:


  x = np.where(movies['genre'] == 'Adventure')

  #print(x)
  index = x
  adventure= []
  adventure.append(movies.iloc[index])
  #print(adventure)


  # In[46]:


  x = np.where(movies['genre'] == 'Sci-Fi')

  #print(x)
  index = x
  scifi= []
  scifi.append(movies.iloc[index])
  #print(scifi)


  # In[47]:


  x = np.where(movies['genre'] == 'Fantasy')

  #print(x)
  index = x
  fantasy= []
  fantasy.append(movies.iloc[index])
  #print(fantasy)


  # In[48]:


  x = np.where(movies['genre'] == 'Drama')

  #print(x)
  index = x
  drama= []
  drama.append(movies.iloc[index])
  #print(drama)


  # In[52]:


  x = np.where(movies['genre'] == 'Horror')

  #print(x)
  index = x
  horror= []
  horror.append(movies.iloc[index])
  #print(horror)


  # In[49]:


  x = np.where(movies['genre'] == 'History')

  #print(x)
  index = x
  history= []
  history.append(movies.iloc[index])
  #print(history)


  # In[50]:


  happy = [romance, comedy, thriller, action, mystery, adventure, scifi ]


  # In[53]:


  sad = [comedy, fantasy, drama, romance, horror, history, scifi]


  # In[54]:


  positive = len(df[df["Sentiment"]=="Positive"])
  negative = len(df[df["Sentiment"]=="Negative"])
  neutral = len(df[df["Sentiment"]=="Neutral"])

  happyOrSad =[]

  weight = [3,2,1,1,1,1,1]
  if positive > negative:
    i = 0
    for i in range(6):
        happyOrSad.append(happy[i][0].sample(weight[i]))

  elif negative > positive:
    i = 0
    for i in range(6):
        happyOrSad.append(sad[i][0].sample(weight[i]))




  return {
    "tweets":"Total Tweets Extracted for Topic : {} are : {}".format(Topic,len(df.Tweet)),
    "positive":"Total Positive Tweets are : {}".format(positive),
    "negative":"Total Negative Tweets are : {}".format(negative),
    "happyOrSad": happyOrSad,
    # "Total Neutral Tweets are : {}".format(neutral)
  }

  # In[56]:
  #for i in range(6):
      #print(happy[i][0].sample(1))

  # In[ ]:





# In[ ]:

### FLASK APP STARTS HERE #####

from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/static')
def staticContent():
  url_for('static', filename='foo.bar')

@app.route('/', methods =["POST", "GET"])
def home():
  if request.method == "GET":
    return render_template('index.html')

  elif request.method == "POST":
    topic = request.form.get('topic')
    result = mainproject(topic)
    happyOrSad = result["happyOrSad"]
    result.pop("happyOrSad")
    print(result)
    return render_template('result.html', result=result, happyOrSad = happyOrSad)
  else:
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



