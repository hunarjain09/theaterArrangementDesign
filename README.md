# Movie Theater Seating

## Assumptions
1. First Come First Serve (Customer Satisfaction)
2. Three Space Buffer after every reservation
3. Maximizing Customer Satisfaction by filling farthest rows first.
4. To increase safety assigning seats in alternate direction in each row (without skipping entire rows). (Customer Safety)
5. Every single reservation wants consecutive seat arrangement.
6. Multiple IDs after sometime are allowed in the current implementation.

## Instructions
1. Run the assignment.py.
2. Enter the path to the input file.
3. Check the output at the path printed on the command line.


## Considerations
1. If we skip rows then customer satifaction will be compromised. (Idea of filling even rows first and then the odd ones by halving the space).
2. Approach using Priority Queues --> Problems of maintaining two of them.
3. Filling from centers will cause more gaps that's why initialised from ends. 

## Improvements
1. Unit Testing
2. Error Handling


