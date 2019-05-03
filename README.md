The folder HIT_layouts includes the task 1, 2, and 3 layouts.
The HTML in the files is copied into the Design Layout-tab when editing the HIT with the AMT WebUI.
Inputs and outputs for each task (in addition to the general outputs from AMT, e.g. HITId and AssignmentId) is as follows:

Task 1:

	Inputs:
		audioType:
			String such as "audio/wav" describing the audio type. Used as the type parameter for the source element of the HTML audio element.
		audioUrl:
			A link to the audio file, through which it can be streamed. Can be e.g. a share link from Dropbox.
			Used as the src parameter for the source element of the HTML audio element
		unique_id:
			A unique id from https://uniqueturker.myleott.com/. Used to limit workers to 100 HITs/batch.
			
	Outputs:
		audioType:
			Same as above
		audioUrl:
			Same as above
		DescriptionText:
			Annotation from worker.
		Feedback:
			Possible feedback from the worker
		

Task 2:

	Inputs:
		DescriptionText:
			Audio caption annotation from the previous task
		AssignmentId:
			Assignment ID of the submission from which the DescriptionText is from.
		audioType:
			Same as in Task 1
		audioUrl:
			Same as in Task 1
		unique_id:
			Same as in Task 1
		
	Outputs:
		audioType:
			Same as above
		audioUrl:
			Same as above
		og_assign:
			AssignmentId from inputs
		ed_assign:
			Assignment ID of the assignment. (Same as the AssignmentId output from AMT)
		OriginalCaption:
			DescriptionText from inputs.
		EditedCaption:
			Annotation from worker.
		Feedback:
			Same as in Task 1

Task 3:

	Inputs:
		captions:
			Annotations from previous tasks for the audio of this HIT. Captions are separated by "|".
		assignments:
			Assignment IDs of the submissions from which the annotations in captions are from. Separated by "|".
		audioType:
			Same as in Task 1 and 2
		audioUrl:
			Same as in Task 1 and 2
		unique_id:
			Same as in Task 1 and 2
		
	Outputs:
		audioType:
			Same as above
		audioUrl:
			Same as above
		captions:
			Same as above
		fluency_scoreX:
			Score for fluency for caption X, annotated by the worker
		accuracy_scoreX:
			Score for accuracy for caption X, annotated by the worker
		fluency_scores:
			Fluency score annotations for captions separated by "|"
		accuracy_scores:
			Accuracy score annotations for captions separated by "|".
		Feedback:
			Same as in Task 1 and 2



db_links.py creates share links from files in a Dropbox folder. Links are stored in a csv file, which is written on disk and uploaded to Dropbox.
