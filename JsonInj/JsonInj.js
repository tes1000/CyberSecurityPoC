  const express = require("express");
    const app = express();
    const bodyParser = require("body-parser");
    const cors = require("cors");
    const json5 = require("json5");

    var persons = [];
    class Person {
              constructor(obj) {
                this.username = obj.username;
                this.password = obj.password;
                this.admin = obj.admin;

                persons.push(this);
                this.login = this.login.bind(this)
    }
      login(username, password) {
                if (username === this.username && password === this.password) {
                  console.log("Login successful");
          return true;
      } else {
                  console.log("Login failed. Please check your username and password.");
          return false;
      }
    }
  }

    var Bob = new Person({username: "Bob", password:"SupersEcretpaSsphraSe!", admin: false})
    console.log(Bob)

    app.use(bodyParser.urlencoded({ extended: true }));
    app.use(cors()); // Enable CORS for all routes
    app.use((req, res, next) => {
        if (req.headers["content-type"] === "application/json" || req.headers["content-type"] === "application/json5") {
          try {
            let data = "";
          req.on("data", (chunk) => {
              data += chunk;
        });
          req.on("end", () => {
              //console.log("DATA: ", data)
            req.body = json5.parse(data);
            //console.log("REQBOD: ",req.body)
            next();
        });
      } catch (error) {
            return res.status(400).json({ error: "Invalid JSON or JSON5 payload" });
      }
    } else {
          next();
    }
  });
    app.get("/", (req, res) => {
          // Add a login form
        res.send(`
        <h1>Login Form</h1>
        <ul>Bobs Login details have Leaked online, Use Json Injection to priv esc!</ul>
        <p>Username: Bob \n Password: SupersEcretpaSsphraSe!<p><br/>
        <form id="loginForm">
          <label for="username">Username:</label>
          <input type="text" id="username" name="username" required><br>
          <label for="password">Password:</label>
          <input type="password" id="password" name="password" required><br>
          <button type="button" onclick="submitForm(&quot;login&quot;)">Login</button>
        </form>
        <div id="loginResult"></div>
        <br/><br/><br/>
        <script>
          function submitForm(action) {
              var form = document.getElementById("loginForm");
            var formData = {
                username: form.elements.username.value,
              password: form.elements.password.value,
          };
      
            var endpoint = "login";
      
            fetch(endpoint, {
                method: "POST",
              headers: {
                  "Content-Type": "application/json",
            },
              body: JSON.stringify(formData),
          })
            .then(response => response.json())
            .then(data => {
                var loginResultDiv = document.getElementById("loginResult");
              loginResultDiv.innerHTML = JSON.stringify(data);
          })
            .catch(error => console.error("Error:", error));
        }
        </script>
        `);
    });
    // LOGIN
    app.post("/login", (req, res) => {
        validInput=inputValidation(req.body)
      if (!validInput[0]){
          res.status(403).send({msg: validInput[1]})
    } else {
        const user1 = req.body;
      if(persons.find(person => person.username === user1.username && person.password === user1.password)) {
          if (user1.admin) {
            res.json({ Flag: "M*zrJTk4uddNk2b2uUz@XAnYARsxEmY55y*JDM4YM8mVBVc7!3w%C4SU" });
      } else {
            res.json({ username: user1.username, admin: user1.admin, msg: "You will need admin access to see the flag." });
      }
    } else {
          res.status(400).json({ message: "Login failed. Please check your username and password." });
    }
  }});

    // start the server
    function inputValidation(input){
        pattern = /^[a-zA-Z0-9_\-!@#$%^&*()+=?<>:.,;{}[\]|\s]+$/;
      if(typeof(input) != "object")
        return [false, "Input Error: Not Object"]
      if(!Object.keys(input).includes("username") || !Object.keys(input).includes("password"))
        return [false, "Input Error: username or password missing"]
      //if(Object.keys(input).includes("admin"))
        //return [false, "Access Denied: We dont allow self made admin!"]
      if (!pattern.test(input.username) || !pattern.test(input.password))
        return [false, "Input Error: username and password must match /^[a-zA-Z0-9_\-!@#$%^&*()+=?<>:.,;{}[\]|\s]+$/"];
      return [true]
  }
    app.listen(3000, () => {
        console.log("Server is running on port 3000");
  });
  