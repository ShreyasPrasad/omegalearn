// Initialize an OpenTok Session object
var session = OT.initSession(apiKey, sessionId);

// Initialize a Publisher, and place it into the element with id="publisher"
var publisher = OT.initPublisher('publisher');

// Attach event handlers
session.on({

  // This function runs when session.connect() asynchronously completes
  sessionConnected: function(event) {
    // Publish the publisher we initialzed earlier (this will trigger 'streamCreated' on other
    // clients)
    session.publish(publisher, function(error) {
      if (error) {
        console.error('Failed to publish', error);
      }
    });

    // Center the user's video
    let ddiv = document.querySelector('body>div'); // $x('/html/body/div')
    let vid_container = document.getElementById("videos");
    // vid_container.appendChild(ddiv)
    vid_container.insertBefore(ddiv, document.getElementById("subscribers"));
  },

  // This function runs when another client publishes a stream (eg. session.publish())
  streamCreated: function(event) {
    // Create a container for a new Subscriber, assign it an id using the streamId, put it inside
    // the element with id="subscribers"
    var subContainer = document.createElement('div');
    subContainer.id = 'stream-' + event.stream.streamId;
    document.getElementById('subscribers').appendChild(subContainer);

    // Subscribe to the stream that caused this event, put it inside the container we just made
    session.subscribe(event.stream, subContainer, function(error) {
      if (error) {
        console.error('Failed to subscribe', error);
      }
    });
  }

});

// Connect to the Session using the 'apiKey' of the application and a 'token' for permission
session.connect(token, function(error) {
  if (error) {
    console.error('Failed to connect', error);
  }
});
