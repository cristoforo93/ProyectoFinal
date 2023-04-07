DDL_QUERY = '''
CREATE TABLE mytable(
   Game_id         INTEGER  NOT NULL PRIMARY KEY 
  ,Name            VARCHAR(132)
  ,Platform        VARCHAR(4) NOT NULL
  ,Year_of_Release VARCHAR(4) NOT NULL
  ,Genre           VARCHAR(12)
  ,Publisher       VARCHAR(38) NOT NULL
  ,NA_Sales        NUMERIC(5,2) NOT NULL
  ,EU_Sales        NUMERIC(5,2) NOT NULL
  ,JP_Sales        NUMERIC(5,2) NOT NULL
  ,Other_Sales     NUMERIC(5,2) NOT NULL
  ,Global_Sales    NUMERIC(5,2) NOT NULL
  ,Critic_Score    INTEGER 
  ,Critic_Count    INTEGER 
  ,User_Score      NUMERIC(3,1)
  ,User_Count      INTEGER 
  ,Developer       VARCHAR(80)
  ,Rating          VARCHAR(4)
);
'''