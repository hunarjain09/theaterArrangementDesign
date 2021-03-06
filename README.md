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
1. Thought of an approach of using Priority Queue but the complexity will be O(nlogn).
2. Filling from centers will cause more gaps that's why initialised from ends. 

## Improvements
1. Better Unit Testing
2. Better Error Handling

## Flow Diagram

![Flow Diagram](./seatingArrangement.svg)
