bids ={}
bidding_finished = False

def highest(record):
 highest_bid = 0
 winner=" "
 for bidder in record:  
   bid_amount = record[bidder]
   if bid_amount> highest_bid:
        highest_bid=bid_amount
        winner = bidder
 print(f"The winner is {winner} with a bid of {highest_bid} ")

while not bidding_finished:

    name =input("What is Your Name : ")
    price =int(input("Enter tHe Bid Price:Rs "))
    bids[name] = price
    other_bidders =input("Are There any Other Bidders? Types Yes or No ")
    if other_bidders == "no":
        bidding_finished=True
        highest(bids)
    elif other_bidders == "yes":
     pass
 