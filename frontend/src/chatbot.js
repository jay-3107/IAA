class Chatbox {
  constructor() {
    // Store references to elements and loader for easy access
    this.args = {
      openButton: document.querySelector(".chatboxbutton"), // Chatbox toggle button
      chatBox: document.querySelector(".chatboxsupport"), // Chatbox container
      sendButton: document.querySelector(".sendbutton"), // Send button
      loader: document.querySelector(".loader"), // Loader element for spinner
    };

    // State of the chatbox (open/closed)
    this.state = false;
    // Array to store chat messages
    this.messages = [];
  }

  // Initialize event listeners for the chatbox
  display() {
    const { openButton, chatBox, sendButton } = this.args;

    // Toggle the chatbox when the open button is clicked
    openButton.addEventListener("click", () => this.toggleState(chatBox));

    // Send message when the send button is clicked
    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    // Send message when the Enter key is pressed
    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  // Toggle the visibility of the chatbox
  toggleState(chatbox) {
    // Switch the state (open/closed)
    this.state = !this.state;

    // Show the chatbox if open, hide it if closed
    if (this.state) {
      chatbox.classList.add("chatboxactive");
    } else {
      chatbox.classList.remove("chatboxactive");
    }
  }

  // Handle the send button click and send message to API
  onSendButton(chatbox) {
    // Get the message from the input field
    var textField = chatbox.querySelector("input");
    let text1 = textField.value;

    // Do nothing if the input is empty
    if (text1 === "") {
      return;
    }

    // Add the user's message to the message list
    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);

    // Show loader while waiting for a response from the API
    this.showLoader();

    // Send the message to the server
    fetch("/api/ask", {
      method: "POST",
      body: JSON.stringify({
        message: text1, // User's message
        url: "https://www.iaa.edu.in/home", // URL for scraping (as per the RAG logic)
      }),
      mode: "cors", // Cross-origin resource sharing mode
      headers: {
        "Content-Type": "application/json", // Specify the request format as JSON
      },
    })
      .then((r) => r.json()) // Parse the JSON response
      .then((r) => {
        // Add the API response to the message list
        let msg2 = { name: "Sam", message: r.answer };
        this.messages.push(msg2);

        // Update the chatbox with the new messages
        this.updateChatText(chatbox);

        // Clear the input field after sending the message
        textField.value = "";

        // Hide the loader after receiving the response
        this.hideLoader();
      })
      .catch((error) => {
        // Log any errors to the console
        console.error("Error:", error);

        // Update the chatbox to reflect the current messages
        this.updateChatText(chatbox);

        // Clear the input field even if an error occurred
        textField.value = "";

        // Hide the loader in case of an error
        this.hideLoader();
      });
  }

  // Update the chatbox with the current list of messages
  updateChatText(chatbox) {
    var html = "";

    // Reverse loop through messages and format them for display
    this.messages
      .slice()
      .reverse()
      .forEach(function (item, index) {
        if (item.name === "Sam") {
          // Message from "Sam" (API response)
          html +=
            '<div class="messagesitem messagesitemvisitor">' +
            item.message +
            "</div>";
        } else {
          // Message from "User"
          html +=
            '<div class="messagesitem messagesitemoperator">' +
            item.message +
            "</div>";
        }
      });

    // Display the formatted messages in the chatbox
    const chatmessage = chatbox.querySelector(".chatboxmessages");
    chatmessage.innerHTML = html;
  }

  // Show the loading spinner when waiting for a response
  showLoader() {
    this.args.loader.style.display = "block"; // Set loader to visible
  }

  // Hide the loading spinner after response or error
  hideLoader() {
    this.args.loader.style.display = "none"; // Set loader to hidden
  }
}

// Instantiate the Chatbox class and display the chatbox
const chatbox = new Chatbox();
chatbox.display();
