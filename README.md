# quiz-quesbank-management

This is a test project to manage the questions that my friend and I write for the quizzes we do. The initial working version is going to be simpler and easier in its scope, it will be aimed only at managing the questions and associate them with the ideas.

## Current Situation

Everything is basically being shuffled between a Word document and an Excel spreadsheet. There's a need to change that using a website that updates the database but also gives a interface that acts both as the Word document and automatically adds the question to the database. This will make referencing easy as well, with the questions becoming easier to fetch and eliminating the need for Excel and Word.

## Database Details

### List of Tables

The following are the tables in the database:

* ```question_ideas```: a table to store the list of ideas
* ```questions_data```: this contains the list of questions. Probably the most expansive of the lot.
* ```question_versions```: old versions of questions. Ideally this specific data is not very important but it is a nice thing to have just in case. It's not a nice to have, this is to be implemented for sure.
* ```question_categories```: categories and subcategories associated with each question.
* ```categories```: only categories stored and corresponding unique IDs.
* ```subcategories```: subcategories with unique IDs and associated with a category.
* ```quizzes```: table to store information about the quizzes conducted.
* ```notes```: store different ideas for quizzes that can be referred to later when quizzes are being created or conducted.


### Table Details

Cell information mandatory unless specified otherwise.

#### ```question_ideas```
* ```idea_index```: \[```int```\] unique identifier of idea.
* ```idea_fact```: \[```str```\] the fact or idea for the question.
* ```sources```: \[```str```\]\[```optional```\] resources for the relevant information to frame the question.
* ```is_framed```: \[```bool```\] to determine if a question is already framed or not.

#### ```questions_data```
* ```question_index```: \[```int```\] unique identifier for the question, this has to be tied into a corresponding idea in the ```questions_ideas``` table.
* ```question_text```: \[```str```\] the actual text of the question.
* ```answer_text```: \[```str```\] the actual text of the answer.
* ```answer_explanation```: \[```str```\]\[```optional```\] any explanation to supplement the answer.
* ```idea_index```: \[```int```\]\[```optional```\] the index of the corresponding idea from the ```questions_ideas``` table will populate this column.
* ```question_create_date```: \[```timestamp```\] the timestamp for the creation of the question.
* ```owner```: \[```str```\] the creator/writer of the question.
* ```categories```: \[```list```\] multiple integers dedicated to the category of the question.
* ```subcategories```: \[```list```\] multiple integers dedicated to the subcategory of the question. 
* ```media```: \[```str```\] comma separated filenames of the media used in the question and answer.
* ```type```: \[```str```\] written as a solo or a themed round question.
* ```used_in```: \[```str```\] comma separated list of quiz identifiers that the question was used in.
* ```version_number```: \[```int```\] the incarnation of the question in the table.
* ```record_create_date```: \[```timestamp```\] the date of the creation of the record.
* ```record_updation_date```: \[```timestamp```\] the last updated timestamp of the record.

#### ```question_categories```
* ```question_id```: \[```int```\] unique identifier for the question, this has to be tied into a corresponding question in the ```questions_data``` table.
* ```category_id```: \[```int```\] unique index to identify the category, this has to be tied into a corresponding category in the ```categories``` table.
* ```subcategory_id```: \[```int```\] unique index to identify the subcategory, this has to be tied into a corresponding subcategory in the ```subcategories``` table.

#### ```question_versions```
* ```question_index```: \[```int```\] unique identifier for the question, this has to be tied into a corresponding question in the ```questions_data``` table.
* ```question_text```: \[```str```\] the actual text of the question.
* ```answer_text```: \[```str```\] the actual text of the answer.
* ```answer_explanation```: \[```str```\]\[```optional```\] any explanation to supplement the answer.
* ```idea_index```: \[```int```\]\[```optional```\] the index of the corresponding idea from the ```questions_ideas``` table will populate this column.
* ```question_create_date```: \[```timestamp```\] the timestamp for the creation of the question.
* ```owner```: \[```str```\] the creator/writer of the question.
* ```categories```: \[```list```\] multiple integers dedicated to the category of the question.
* ```subcategories```: \[```list```\] multiple integers dedicated to the subcategory of the question. 
* ```media```: \[```str```\] comma separated filenames of the media used in the question and answer.
* ```type```: \[```str```\] written as a solo or a themed round question.
* ```used_in```: \[```str```\] comma separated list of quiz identifiers that the question was used in.
* ```version_number```: \[```int```\] the incarnation of the question in the table.
* ```record_create_date```: \[```timestamp```\] the date of the creation of the record.
* ```record_updation_date```: \[```timestamp```\] the last updated timestamp of the record.

#### ```categories```
* ```category_index```: \[```int```\] unique index to identify the category.
* ```category_name```: \[```str```\] name of the category.

#### ```subcategories```
* ```subcategory_index```: \[```int```\] unique index to identify the subcategory.
* ```subcategory_name```: \[```str```\] name of the subcategory.
* ```category_index```: \[```int```\] corresponding category index.

#### ```quizzes```
* ```quiz_index```: \[```str```\] unique identifier for the quiz in question.
* ```quiz_event```: \[```str```\]\[```optional```\] a type for the quiz, if there is any any.
* ```quiz_title```: \[```str```\]\[```optional```\] name of the final quiz.
* ```quizmasters```: \[```str```\] comma separated list of quizmasters.
* ```date_of_quiz```: \[```timestamp```\] the date of the event.
* ```question_count```: \[```int```\] the number of questions in the quiz.
* ```teams_count```: \[```int```\]\[```optional```\] the number of teams in the quiz.
* ```max_possible_score```: \[```float```\]\[```optional```\] the highest possible score that can be attained in the quiz.
* ```first_place_score```: \[```float```\]\[```optional```\] score of the first place holder.
* ```second_place_score```: \[```float```\]\[```optional```\] score of the second place holder.
* ```third_place_score```: \[```float```\]\[```optional```\] score of the third place holder.
* ```reception```: \[```str```\] a general overview of how the quiz was received.
* ```remarks```: \[```str```\] any remarks about the conducting of the quiz.

#### ```notes```
* ```note_text```: \[```str```\] the actual note that is to be stored.
* ```record_create_date```: \[```timestamp```\] the timestamp of the record creation.
* ```record_updation_date```: \[```timestamp```\] the timestamp of the latest updation of the record.

### Relational Diagram

![Relational diagram of the database](relational_diagram.png)

ER diagram created using [dbdiagram.io](https://dbdiagram.io).

The foreign keys and the relation types are also specified.

## Different Pages

The following pages are needed:
* **Login**: The login page is the landing page.
* **Display**: Display pages for the following:
	* Display list of ideas
	* Display list of questions
	* Display list of quizzes
	* Display notes
* **Insert**: Pages to insert new records for the following:
	* Insert new idea
	* Insert new question
	* Insert new quiz
	* Write new notes
* **Update**: Pages to update the records for the following:
	* Update existing idea
	* Update a question
	* Update quiz details
	* Update a note 