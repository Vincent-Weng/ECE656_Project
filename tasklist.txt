Part I. Data preprocessing
    [x] 1.1 E-R diagram
            - Requirement: primary keys, entity relationships, cardinality constraints
    [ ] 1.2 Data cleaning: sanity checking and consistency checking.
            - Requirement: as much as possible
        [ ] - Jupyter notebook Part 1: do the sanity/consistency checking
        [ ] - Recommend solutions for such situations
        1.3 Data indexing:
            - Should be done after 1.4
        [ ] - Jupyter notebook Part 2: Compare the timing results with/without indices and keys. For the "without" part, all keys and indices should be removed. Screenshots and analysis should be included in the final report.
        1.4 Analyze data 
        [ ] - Jupyter notebook: perform the processing
        [ ] - Use half of data to do the prediction, and verify it using the other half
            - potentialSpamUser: 
                - short ageBeforeReview
                - revStar == 1 or 5, avgRevStar == 1 or 5
                - revCount == 1
                - `useful` and `funny` and `cool` == 0
                - no fans
            - potentialSpamBusiness:
                - have many potentialSpamUser reviews
                - high review `text` similarity

Part II. Application privilege control
    [ ] 2.1 Analyze these groups of users, determine the least privilege they should be granted to use Yelp.
        1. A casual user who uses the application to browse search results. These users do not need to have an account; hence, they cannot submit reviews.
        2. Critiques that use the application to browse results just like the casual user, but they also leave reviews for places they visit. A logged in user should only be provided enough priv- ileges to write the review.
        3. Business analysts can use the application to produce sales reports and may want to do special data mining and analysis. They cannot perform IUD (Insert/Update/Delete) opera- tions on the database but should have access to creating extra views on the database schema.
        4. Developers working with this database are able to create new tables and perform data cleaning and indexing. They are allowed to perform IUD operations on the database.
        5. The database admin who has full access over the database.
    [ ] 2.2 Create the corresponding SQL queries to grant permissions.

Part III. Write the report

