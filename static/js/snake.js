$(document).ready(function() {
			var canvas = $('#canvas')[0];
			var ctx = canvas.getContext('2d');
			var w = canvas.width;
			var h = canvas.height;
			var cw = 10;
			var d;
			var food;
			var score;
			var snake_array;
			var speed;
			var high_score;
			var username;
//			window.location.port = '5000';
//            window.location.protocol = 'http:';
//            window.location.hostname = 'snake-game';

//            const baseUrl = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
//            const baseUrl = "http://snake-game:5000";

			async function get_high_score(user_name) {
              try {
                const response = await $.ajax({
                  type: "GET",
                  url: "/high_score/" + user_name,
//                  url: baseUrl + "/high_score/" + user_name,
                  dataType: "json"
                });
                console.log("User's previous high score: " + response);
                return response || 0;
              } catch (error) {
                console.log(error);
                return 0;
              }
            }

			function init(high_score, username) {
            console.log("init")
            console.log(`${high_score}`)
                messageBox.textContent = "Click on the board to play";
                $('#canvas').click(function() {
                messageBox.textContent = "";

                d = 'right';
				create_snake();
				create_food();
				score = 0;

				if (typeof game_loop != 'undefined') clearInterval(game_loop);
				speed = 150;

                game_loop = setInterval(() => {
                    paint(username, high_score);
                }, speed);
			                    });
			}

			function update_speed(score, high_score) {
			console.log("update_speed")
            console.log(`${high_score}`)

			  if (score < 10) {
				speed = speed - 10;
			  } else if (score < 20) {
				speed = speed -5;
			  } else if (score < 30) {
				speed = speed -1;
			  }
			  clearInterval(game_loop);
                game_loop = setInterval(() => {
                    paint(username, high_score);
                }, speed);
                }

			function create_snake() {
				var length = 5;
				snake_array = [];
				for (var i = length - 1; i >= 0; i--) {
					snake_array.push({x: i, y: 0});
				}
			}

			function create_food() {
				food = {
					x: Math.round(Math.random() * (w - cw) / cw),
					y: Math.round(Math.random() * (h - cw) / cw),
				};
			}

function paint(username, high_score) {
    console.log("paint")
    console.log(`${high_score}`)
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = 'white';
    ctx.strokeRect(0, 0, w, h);

    var nx = snake_array[0].x;
    var ny = snake_array[0].y;

    if (d == 'right') nx++;
    else if (d == 'left') nx--;
    else if (d == 'up') ny--;
    else if (d == 'down') ny++;

    if (nx < 0) {
        nx = w/cw - 1;
    } else if (nx > w/cw - 1) {
        nx = 0;
    } else if (ny < 0) {
        ny = h/cw - 1;
    } else if (ny > h/cw - 1) {
        ny = 0;
    }

    if (check_collision(nx, ny, snake_array)) {
        console.log(`check score with Username: ${username} and Score: ${score}`);
        clearInterval(game_loop);
        if (score > high_score) {
            $('#high_score').html(score);
            console.log(`Submitting score with Username: ${username} and Score: ${score}`);
            submit_score(username, score)
        }
        init(score, username);
        return;
    }

    if (nx == food.x && ny == food.y) {
        var tail = {x: nx, y: ny};
        score++;
        create_food();
        update_speed(score, high_score);
    } else {
        var tail = snake_array.pop();
        tail.x = nx;
        tail.y = ny;
    }

				snake_array.unshift(tail);

				for (var i = 0; i < snake_array.length; i++) {
					var c = snake_array[i];
					paint_cell(c.x , c.y, 'white');
                }
        			paint_cell(food.x, food.y, 'red');

			$('#score').html(score);
		}

		function paint_cell(x, y, colour) {
			ctx.fillStyle = colour;
			ctx.fillRect(x * cw, y * cw, cw, cw);
			ctx.strokeStyle = 'black';
			ctx.strokeRect(x * cw, y * cw, cw, cw);
		}

		function check_collision(x, y, array) {
			for (var i = 0; i < array.length; i++) {
				if (array[i].x == x && array[i].y == y) return true;
			}
			return false;
		}

		async function submit_score(username, score) {
		    var data = {
        "username": username,
        "score": score
    };

		    await $.ajax({
        type: "POST",
        url: "/submit",
//        url: baseUrl + "/submit",

        contentType: "application/json",
      data: JSON.stringify(data),
        success: function(response) {
            // handle the server's response here
        },
        error: function(error) {
            console.log(error);
        }
    });
    }




$(document).on({
  'touchstart': function(e) {
    touchStartX = e.changedTouches[0].pageX;
    touchStartY = e.changedTouches[0].pageY;
  },
  'touchmove': function(e) {
    e.preventDefault();
    touchEndX = e.changedTouches[0].pageX;
    touchEndY = e.changedTouches[0].pageY;
    handleSwipe();
  }
});

function handleSwipe() {
  var xDiff = touchStartX - touchEndX;
  var yDiff = touchStartY - touchEndY;
  if (Math.abs(xDiff) > Math.abs(yDiff)) {
    if (xDiff > 0 && d != 'right') d = 'left';
    else if (xDiff < 0 && d != 'left') d = 'right';
  } else {
    if (yDiff > 0 && d != 'down') d = 'up';
    else if (yDiff < 0 && d != 'up') d = 'down';
  }
}

$(document).keydown(function(e) {
  var key = e.which;
  if (key == '37' && d != 'right') d = 'left';
  else if (key == '38' && d != 'down') d = 'up';
  else if (key == '39' && d != 'left') d = 'right';
  else if (key == '40' && d != 'up') d = 'down';
});

        var messageBox = document.getElementById("message-box");

        const form = document.getElementById('username-form');

            form.addEventListener('submit', (event) => {
                event.preventDefault();
                username = document.getElementById('username').value;

                if (username.length < 1) {
                    messageBox.textContent = "'Please enter a valid username.'";
                    alert('Please enter a valid username.');
                } else {
                    messageBox.textContent = "Click on the board to play";
                    get_high_score(username)
                                      .then(high_score => {
                                        console.log("User's high score: " + high_score);
                                        $('#high_score').html(high_score); //todo method
                                    console.log(`Starting game with username: ${username}  and high score: ${high_score}`);
                                    init(high_score, username);
                                      })


                }
            });


	});