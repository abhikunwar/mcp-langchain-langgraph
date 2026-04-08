function greet(name) {

    return "hello" + name

}

console.log(greet(" abhishek"))

// exercise 2
let name = "Abhishek"
name = "Rahul"
console.log(name)

// exercise 3 : add two numbers

function add_number(a,b){
    
     
    return a +b
}
console.log(add_number(2,3))


// excercise 4: print message one by one
message = ['hello','how are you']
message.map((msg)=>console.log(msg))

// display the log message
const messages = [
  { sender: "user", text: "Hi!" },
  { sender: "bot", text: "Hello!" }
];

messages.map(msg => console.log(msg))

// push new message like aimessage
let messages1 = [
  { sender: "user", text: "Hi!" }
]
messages.push({sender: "user", text: "Hello!"})
