## task1
### プロンプト例①
```
Background:
The "Booking Blunder" villain has been causing chaos in the hotel booking process, leading to confusion, double bookings, and frustrated customers. This villain thrives on ambiguity and unclear communication, making it challenging for hotels to manage their reservations effectively.

Business Use Case
A prominent hotel chain has been grappling with the consequences of the "Booking Blunder" villain's mischief. They need a solution to streamline their booking process and provide clear and concise information to customers during the reservation process.

To defeat the "Booking Blunder" villain, you will need to craft a COSTAR prompt that helps the hotel chain provide clear and concise information to customers during the booking process.

Your Task
Your task is to craft a prompt which will generate a booking confirmation message that includes the following information:

Customer's name
Check-in and check-out dates
Room type
Total cost
Cancellation policy
Contact information for the hotel
```

### プロンプト例②
```
You are a reservation manager for a hotel that has been affected by the "Booking Blunder" villain, causing significant issues in the booking process. Generate a booking confirmation message that specifically addresses these problems. The message should be objective, formal, professional, and concise. Ensure the tone is polite, courteous, reassuring, and empathetic, acknowledging the recent issues caused by the Booking Blunder villain. The audience for your message is customers in our gold membership program. The results should be a final comprehensive message with their booking details, aimed at restoring their confidence in our booking process.
```

## task2
### プロンプト例①
```
Background
The "Flight Fiasco" is a nefarious villain who has been wreaking havoc on airline schedules, causing widespread delays and cancellations. This chaos has led to frustration among travelers and significant financial losses for airlines. The villain's motives are unknown, but their ability to disrupt flight operations with precision and stealth has left authorities baffled.

Business Case
The airline industry has been struggling to cope with the Flight Fiasco's attacks, which have resulted in substantial revenue losses and a tarnished reputation. Customers are losing faith in the airlines' ability to provide reliable service, and the industry's credibility is at stake. To combat this threat, a team of data scientists and AI experts has been assembled to develop a solution that can predict and mitigate the impact of the Flight Fiasco's actions. Flight Fiasco's attacks are corrupting the reservation that that's exchanged between reservation and confirmation systems, causing these system to break and causing customers to not get their tickets in time.

Your Task
Your task is to stop Flights Fiasco attacks and organize the reservation confirmation booking messages. You need to give the model the right examples in the prompt so the confirmation contains all information from the customer, their flight number, departure date and all details required for a flight and it should be in a fixed format of your choice.
```

### プロンプト例②
```
Context: Due to the recent attacks by the villain Flight Fiasco, our airline has experienced substantial revenue losses and a tarnished reputation. Customers are losing faith in our ability to provide reliable service, and the industry's credibility is at stake. To regain customer trust, we need to ensure that our reservation confirmation messages are clear, reassuring, and contain all necessary information. Objective (O): Generate a fixed-format reservation confirmation message for customers booking their flights. Style (S): The message should be written in a formal and concise style. Tone (T): The tone should be professional and reassuring to help rebuild customer trust. Audience (A): The intended audience is airline customers. Response (R): The confirmation message should be in text format and include the following details: customer name, flight number, departure date, departure time, arrival date, arrival time, departure airport, arrival airport, seat number, and any special instructions. Example Output: Reservation Confirmation Dear [Customer Name], Thank you for booking your flight with [Airline Name]. Below are the details of your reservation: Flight Number: [Flight Number] Departure Date: [Departure Date] Departure Time: [Departure Time] Arrival Date: [Arrival Date] Arrival Time: [Arrival Time] Departure Airport: [Departure Airport] Arrival Airport: [Arrival Airport] Seat Number: [Seat Number] Special Instructions: [Any Special Instructions] We appreciate your business and are committed to providing you with a reliable and enjoyable travel experience. If you have any questions or need further assistance, please contact our customer service at [Customer Service Contact Information]. Safe travels, [Airline Name] Customer Service Team
```

## task3
### プロンプト例①
```
Background
The "Restaurant Ruckus" villain has been causing chaos in the restaurant industry, leading to disastrous dining experiences and frustrated patrons. This nefarious character has the ability to manipulate reservation systems, resulting in double bookings, incorrect orders, and overall mayhem. To vanquish this villain and restore order to the culinary world, we must harness the power of chain of thought prompting.

The villain has struck again, this time at the popular restaurant "Flavors of the World." The staff is overwhelmed with a series of issues caused by the villain's meddling:

Business Case
Restaurants are struggling to provide seamless experiences for their customers due to the "Restaurant Ruckus" villain's interference. Incorrect reservations, mixed-up orders, and disgruntled patrons are leading to negative reviews, lost revenue, and a tarnished reputation. By implementing chain of thought prompting, restaurants can streamline their processes, enhance customer satisfaction, and ultimately triumph over this troublesome villain's actions:

Double bookings: Several tables have been double-booked, leading to confusion and frustration among customers.
Incorrect orders: Numerous orders have been mixed up, with customers receiving dishes they didn't order.
Your Task
Your mission, should you choose to accept it, is to create a chain of thought prompt that will guide the restaurant staff in resolving common issues caused by the "Restaurant Ruckus" villain. This prompt should break down the problem-solving process into smaller, logical steps, allowing the staff to reason through each step and arrive at an effective solution.
```

### プロンプト例②
```
This is a complex situation for an LLM so solve in a single shot and even adding examples would potentially create innacurate responses. This is where Chain of Thoughts becomes important. Breaking the step into logical steps and guideling the model on how to do this using Prompt Engineering. An example of prompt could look like this:

"You are a restaurant manager and you need to help fix problems with reservations for the dinner rush. The issues are related to incorrect dishes assigned to guests with special requests and double bookings for the same table. You need to take the following steps to fix these problems: You must not create a code, you need to sort through this list of steps yourself.

Analyze the data set and identify each specific reservation that has incorrect orders where the Pre-ordered dish does not match the Special Requests.
Once the incorrect reservations are identified, assign new dishes to each reservation based on the special requests.
After having the updates reservations with the new dishes, go through the tables assigned to each reservation on the and identify any double bookings.
Once the double bookings are identified, rearrange the seating tables so that there are no double bookings.
Your output should be a new csv data set containing the corrected orders and seating arrangements, do not add anything else on your output, just the new CSV.
Name,Date,Time,Party Size,Special Requests,Pre-ordered Dishes,Table John Smith,5/15/23,19:00,4,Vegetarian,Grilled Chicken Breast; Caprese Salad,Table 1 Emma Johnson,5/15/23,19:30,2,Gluten-free,Spaghetti Carbonara; Garlic Bread,Table 2 Michael Brown,5/15/23,20:00,6,None,Beef Stroganoff; Caesar Salad,Table 3 Sarah Davis,5/15/23,18:45,3,Nut allergy,Almond-crusted Salmon; Mixed Greens,Table 4 David Wilson,5/15/23,19:15,5,Vegan,Butter Chicken; Naan Bread,Table 5 Lisa Anderson,5/15/23,20:30,2,Lactose-intolerant,Four Cheese Pizza; Tiramisu,Table 6 Robert Taylor,5/15/23,18:30,4,Kosher,Pork Schnitzel; Potato Salad,Table 7 Jennifer Martinez,5/15/23,19:45,3,Pescatarian,Grilled Steak; Roasted Vegetables,Table 8 William Lee,5/15/23,20:15,2,Halal,Wine-braised Short Ribs; Mashed Potatoes,Table 1 Elizabeth Clark,5/15/23,19:00,6,Low-sodium,Salt-cured Ham; Pickled Vegetables,Table 9 Thomas Rodriguez,5/15/23,18:45,4,Shellfish allergy,Shrimp Scampi; Clam Chowder,Table 10 Mary White,5/15/23,20:45,2,Diabetic,Sugar-glazed Donuts; Sweet Tea,Table 2 Daniel Harris,5/15/23,19:30,5,Egg allergy,Quiche Lorraine; Egg Salad Sandwich,Table 11 Patricia Lewis,5/15/23,20:00,3,Soy-free,Tofu Stir-fry; Soy Sauce Chicken,Table 3 Christopher Hall,5/15/23,18:30,4,Paleo,Cheese Ravioli; Garlic Bread,Table 12 Margaret Young,5/15/23,19:15,2,Low-carb,Loaded Baked Potato; Pasta Primavera,Table 5 Joseph King,5/15/23,20:30,6,Keto,Rice Pilaf; Sweetened Fruit Salad,Table 13 Nancy Scott,5/15/23,19:45,3,FODMAP,Onion Soup; Garlic Shrimp,Table 8 Kevin Green,5/15/23,18:45,4,Celiac disease,Beer-battered Fish; Wheat Crackers,Table 14 Susan Baker,5/15/23,20:15,2,No spicy food,Ghost Pepper Wings; Jalapeno Poppers,Table 1

{ "appetizers": [ { "name": "Caprese Salad", "description": "Fresh mozzarella, tomatoes, and basil drizzled with balsamic glaze", "price": 9.99, "dietary": ["vegetarian", "gluten-free"] }, { "name": "Mixed Green Salad", "description": "Assorted greens with vinaigrette dressing", "price": 7.99, "dietary": ["vegan", "gluten-free", "nut-free", "low-sodium"] }, { "name": "Steamed Edamame", "description": "Lightly salted soybean pods", "price": 6.99, "dietary": ["vegan", "gluten-free", "low-carb"] }, { "name": "Garlic Shrimp", "description": "Sautéed shrimp in garlic and olive oil", "price": 12.99, "dietary": ["gluten-free", "pescatarian"] } ], "main_courses": [ { "name": "Grilled Chicken Breast", "description": "Herb-marinated chicken breast with roasted vegetables", "price": 18.99, "dietary": ["gluten-free", "low-carb"] }, { "name": "Vegetable Stir-Fry", "description": "Assorted vegetables in a light soy-ginger sauce", "price": 14.99, "dietary": ["vegan", "low-sodium"] }, { "name": "Grilled Salmon", "description": "Fresh salmon fillet with lemon-dill sauce", "price": 22.99, "dietary": ["gluten-free", "pescatarian", "keto"] }, { "name": "Beef Stroganoff", "description": "Tender beef in a creamy mushroom sauce over egg noodles", "price": 20.99, "dietary": [] }, { "name": "Eggplant Parmesan", "description": "Breaded eggplant slices with marinara sauce and melted cheese", "price": 16.99, "dietary": ["vegetarian"] }, { "name": "Quinoa Stuffed Bell Peppers", "description": "Bell peppers filled with quinoa, vegetables, and herbs", "price": 15.99, "dietary": ["vegan", "gluten-free", "low-sodium"] }, { "name": "Lamb Kebabs", "description": "Grilled lamb skewers with tzatziki sauce", "price": 23.99, "dietary": ["gluten-free", "keto"] } ], "side_dishes": [ { "name": "Steamed Rice", "description": "Plain steamed white rice", "price": 3.99, "dietary": ["vegan", "gluten-free"] }, { "name": "Roasted Vegetables", "description": "Seasonal vegetables roasted with herbs", "price": 5.99, "dietary": ["vegan", "gluten-free", "low-carb"] }, { "name": "Mashed Potatoes", "description": "Creamy mashed potatoes", "price": 4.99, "dietary": ["vegetarian", "gluten-free"] }, { "name": "Gluten-free Pasta", "description": "Gluten-free pasta with olive oil and herbs", "price": 6.99, "dietary": ["vegan", "gluten-free"] } ], "desserts": [ { "name": "Fresh Fruit Salad", "description": "Assorted seasonal fruits", "price": 7.99, "dietary": ["vegan", "gluten-free", "low-sugar"] }, { "name": "Chocolate Mousse", "description": "Rich and creamy chocolate mousse", "price": 8.99, "dietary": ["vegetarian", "gluten-free"] }, { "name": "Tiramisu", "description": "Classic Italian coffee-flavored dessert", "price": 9.99, "dietary": ["vegetarian"] }, { "name": "Sorbet", "description": "Refreshing fruit sorbet (ask for flavors)", "price": 6.99, "dietary": ["vegan", "gluten-free", "low-sugar"] } ], "beverages": [ { "name": "Fresh Lemonade", "description": "Homemade lemonade with mint", "price": 3.99, "dietary": ["vegan", "gluten-free"] }, { "name": "Iced Tea", "description": "Unsweetened iced tea", "price": 2.99, "dietary": ["vegan", "gluten-free", "low-sugar"] }, { "name": "Sparkling Water", "description": "Carbonated water with a slice of lemon", "price": 2.49, "dietary": ["vegan", "gluten-free", "low-sugar"] }, { "name": "Herbal Tea Selection", "description": "Various caffeine-free herbal teas", "price": 3.49, "dietary": ["vegan", "gluten-free", "low-sugar"] } ] }

"
```

## task4
```
4OITSADFM8N190ST
```
