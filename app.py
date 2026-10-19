import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Subway Surfers: Oggy & Gián", layout="centered"
)

st.title("🏃‍♂️ Subway Surfers: Phiên Bản Chú Gián Né Oggy")
st.write(
    "Dùng phím **Mũi tên Trái / Phải** (hoặc **A / D**) để đổi 3 làn đường và né chướng ngại vật!"
)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #121212;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
            overflow: hidden;
        }
        #gameContainer {
            position: relative;
            text-align: center;
        }
        #gameCanvas {
            border: 4px solid #ff9800;
            background: #2c3e50;
            box-shadow: 0 0 30px rgba(255, 152, 0, 0.6);
            display: block;
        }
        #restartBtn {
            display: none;
            position: absolute;
            top: 55%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 14px 30px;
            font-size: 20px;
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 6px 15px rgba(0,0,0,0.6);
            z-index: 10;
        }
        #restartBtn:hover {
            background-color: #c0392b;
        }
    </style>
</head>
<body>

    <div id="gameContainer">
        <canvas id="gameCanvas" width="450" height="600"></canvas>
        <button id="restartBtn" onclick="resetGame()">Chơi Lại</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const restartBtn = document.getElementById("restartBtn");

        // Tọa độ 3 làn đường (Lane 0: Trái, Lane 1: Giữa, Lane 2: Phải)
        const lanes = [110, 225, 340]; 
        
        // Nhân vật Gián (Chạy phía trước)
        let player = {
            laneIndex: 1, // Bắt đầu ở làn giữa
            y: 480,
            width: 50,
            height: 50,
            targetX: 225,
            x: 225
        };

        let obstacles = [];
        let score = 0;
        let gameOver = false;
        let frameCount = 0;
        let gameSpeed = 5;

        // Hình ảnh sprite (Sử dụng URL sprite nhân vật hoạt hình rõ nét)
        const roachSprite = new Image();
        roachSprite.src = 'https://cdn-icons-png.flaticon.com/512/3468/3468377.png'; // Model nhân vật gián dạng chi tiết

        const trapSprite = new Image();
        trapSprite.src = 'https://cdn-icons-png.flaticon.com/512/2936/2936735.png'; // Model bẫy chuột/chướng ngại vật

        // Điều khiển bàn phím (3 làn: Trái / Phải)
        document.addEventListener("keydown", (e) => {
            if (gameOver) return;
            if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
                if (player.laneIndex > 0) {
                    player.laneIndex--;
                }
            }
            if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
                if (player.laneIndex < 2) {
                    player.laneIndex++;
                }
            }
        });

        function spawnObstacle() {
            let randomLane = Math.floor(Math.random() * 3);
            obstacles.push({
                laneIndex: randomLane,
                y: -80,
                width: 55,
                height: 55,
                speed: gameSpeed
            });
        }

        function update() {
            if (gameOver) return;

            // Hiệu ứng mượt mà khi chuyển làn (Lerp)
            player.targetX = lanes[player.laneIndex];
            player.x += (player.targetX - player.x) * 0.2;

            // Tăng độ khó dần theo điểm
            gameSpeed = 5 + Math.floor(score / 10) * 0.5;

            // Sinh chướng ngại vật theo thời gian
            frameCount++;
            if (frameCount % 50 === 0) {
                spawnObstacle();
            }

            // Cập nhật vị trí chướng ngại vật chạy từ trên xuống (giả lập 3D đường chạy)
            for (let i = 0; i < obstacles.length; i++) {
                let obs = obstacles[i];
                obs.y += obs.speed;

                // Kiểm tra va chạm (Cùng làn và khoảng cách y trùng nhau)
                let obsX = lanes[obs.laneIndex];
                if (
                    obs.laneIndex === player.laneIndex &&
                    player.y < obs.y + obs.height - 15 &&
                    player.y + player.height > obs.y + 15
                ) {
                    gameOver = true;
                    restartBtn.style.display = "block";
                }

                // Vượt qua chướng ngại vật thành công
                if (obs.y > canvas.height) {
                    obstacles.splice(i, 1);
                    score += 1;
                    i--;
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ nền đường tàu / sàn bếp phong cách 3D phối cảnh (Perspective)
            // Màu nền sàn
            ctx.fillStyle = "#34495e";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Vẽ 3 làn đường dạng hình thang (tạo chiều sâu 3D như Subway Surfers)
            ctx.fillStyle = "#2c3e50";
            ctx.beginPath();
            ctx.moveTo(150, 0); ctx.lineTo(300, 0); ctx.lineTo(400, canvas.height); ctx.lineTo(50, canvas.height);
            ctx.fill();

            // Các vạch kẻ phân làn chạy dọc tạo cảm giác chuyển động
            ctx.strokeStyle = "#f1c40f";
            ctx.lineWidth = 4;
            ctx.setLineDash([20, 20]);
            
            // Đường phân cách 1
            ctx.beginPath();
            ctx.moveTo(200, 0); ctx.lineTo(170, canvas.height);
            ctx.stroke();

            // Đường phân cách 2
            ctx.beginPath();
            ctx.moveTo(250, 0); ctx.lineTo(280, canvas.height);
            ctx.stroke();
            ctx.setLineDash([]); // Reset line dash

            // 2. Vẽ Chướng ngại vật (Bẫy chuột / Đồ vật)
            for (let obs of obstacles) {
                let drawX = lanes[obs.laneIndex] - obs.width / 2;
                ctx.drawImage(trapSprite, drawX, obs.y, obs.width, obs.height);
            }

            // 3. Vẽ Nhân vật Chú Gián
            ctx.drawImage(roachSprite, player.x - player.width / 2, player.y, player.width, player.height);

            // 4. Hiển thị Giao diện Điểm số góc trên
            ctx.fillStyle = "#f1c40f";
            ctx.font = "bold 24px Arial";
            ctx.fillText("ĐIỂM: " + score, 20, 35);

            ctx.fillStyle = "#fff";
            ctx.font = "16px Arial";
            ctx.fillText("Tốc độ: " + gameSpeed.toFixed(1) + "x", 20, 65);

            // 5. Màn hình Game Over
            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#e74c3c";
                ctx.font = "bold 30px Arial";
                ctx.textAlign = "center";
                ctx.fillText("BẠN ĐÃ BỊ TÓM!", canvas.width / 2, canvas.height / 2 - 40);

                ctx.fillStyle = "white";
                ctx.font = "20px Arial";
                ctx.fillText("Tổng điểm né tránh: " + score, canvas.width / 2, canvas.height / 2 + 10);
                ctx.textAlign = "left"; // Reset align
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        function resetGame() {
            player.laneIndex = 1;
            player.x = lanes[1];
            obstacles = [];
            score = 0;
            gameSpeed = 5;
            gameOver = false;
            restartBtn.style.display = "none";
        }

        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=620)
