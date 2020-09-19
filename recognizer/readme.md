# Siemens automation circuit recognizer
Special cirtuit recognizer, made for HackZurich 2020, Siemens "Graph the Building" challenge

Honors go to @mahmut-aksakalli for his image recognition studies, which this recognizer is founded on.

## How it works
1) Using block adjacency graph potential components are segmented
2) Components are identified using contour based classification. Classification is done using support vector machine which is trained with HOG descriptors
3) Potential lines are detected using line segment detector algorithm
4) Components and lines are merged into common graph based on connecting coordinates

