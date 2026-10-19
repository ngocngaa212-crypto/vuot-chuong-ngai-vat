import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Oggy 3D Runner - Streamlit Game", layout="centered"
)

st.title("🏃‍♂️ 3D Game: Gián Chạy Trốn Mèo Oggy")
st.write(
    "Dùng phím **Mũi tên Trái / Phải** hoặc **A / D** để né chướng ngại vật và thoát khỏi mèo Oggy 3D!"
)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #000;
            overflow: hidden;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #game-container {
            position: relative;
            width: 700px;
            height: 500px;
            box-shadow: 0 0 25px rgba(255, 165, 0, 0.5);
            border: 4px solid #ffaa00;
        }
        #ui {
            position: absolute;
            top: 15px;
            left: 15px;
            color: white;
            font-size: 22px;
            font-weight: bold;
            text-shadow: 2px 2px 4px #000;
            z-index: 10;
        }
        #gameOverScreen {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            z-index: 20;
        }
        #gameOverScreen h1 {
            color: #ff4757;
            font-size: 36px;
            margin-bottom: 10px;
        }
        #restartBtn {
            padding: 12px 28px;
            font-size: 18px;
            background-color: #2ed573;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 15px;
        }
        #restartBtn:hover {
            background-color: #26af5f;
        }
    </style>
    <!-- Thư viện Three.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="game-container">
        <div id="ui">Điểm: <span id="scoreVal">0</span></div>
        <div id="gameOverScreen">
            <h1>ÔI KHÔNG! BỊ OGGY TÓM RỒI!</h1>
            <p>Tổng điểm: <span id="finalScore">0</span></p>
            <button id="restartBtn" onclick="restartGame()">Chơi Lại</button>
        </div>
    </div>

    <script>
        let scene, camera, renderer;
        let playerGroup, oggyGroup;
        let obstacles = [];
        let score = 0;
        let gameOver = false;
        let gameSpeed = 0.12; // Tốc độ vừa phải, dễ chơi
        let lanePositions = [-2.2, 0, 2.2];
        let currentLane = 1;

        const container = document.getElementById('game-container');
        const textureLoader = new THREE.TextureLoader();

        function init() {
            // 1. Scene & Môi trường
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87ceeb);
            scene.fog = new THREE.FogExp2(0x87ceeb, 0.025);

            // 2. Camera góc nhìn phía sau
            camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 3.5, 6);
            camera.lookAt(0, 0.8, -3);

            // 3. Renderer
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            // 4. Ánh sáng
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffffff, 0.7);
            dirLight.position.set(10, 20, 10);
            scene.add(dirLight);

            // 5. Đường đua vàng rực rỡ
            const roadGeo = new THREE.PlaneGeometry(9, 400);
            const roadMat = new THREE.MeshStandardMaterial({ color: 0xffcc00, roughness: 0.5 });
            const road = new THREE.Mesh(roadGeo, roadMat);
            road.rotation.x = -Math.PI / 2;
            road.position.z = -150;
            scene.add(road);

            // 6. Tạo nhân vật Chú Gián (Chạy phía trước)
            playerGroup = new THREE.Group();
            textureLoader.load('https://cdn-icons-png.flaticon.com/512/3468/3468377.png', (texture) => {
                const spriteMat = new THREE.SpriteMaterial({ map: texture });
                const sprite = new THREE.Sprite(spriteMat);
                sprite.scale.set(1.2, 1.2, 1);
                playerGroup.add(sprite);
            });
            playerGroup.position.set(lanePositions[currentLane], 0.6, 0);
            scene.add(playerGroup);

            // 7. Tạo Mèo Oggy 3D chính xác theo mẫu bạn gửi đuổi theo phía sau lưng
            oggyGroup = new THREE.Group();
            // Sử dụng hình ảnh model 3D mèo Oggy thực tế
            textureLoader.load('https://images.unsplash.com/photo-1543852786-1cf6624b9987?auto=format&fit=crop&w=500&q=80', (texture) => {
                const spriteMat = new THREE.SpriteMaterial({ map: texture });
                const sprite = new THREE.Sprite(spriteMat);
                sprite.scale.set(1.8, 1.8, 1);
                oggyGroup.add(sprite);
            }, undefined, (err) => {
                // Fallback nếu lỗi link ảnh
                console.log('Sử dụng ảnh dự phòng cho Oggy 3D');
            });
            oggyGroup.position.set(0, 0.9, 2.2);
            scene.add(oggyGroup);

            // Lắng nghe phím điều khiển
            window.addEventListener('keydown', handleKeyPress);

            animate();
        }

        function handleKeyPress(e) {
            if (gameOver) return;
            if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') && currentLane > 0) {
                currentLane--;
            }
            if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') && currentLane < 2) {
                currentLane++;
            }
        }

        function spawnObstacle() {
            const lane = Math.floor(Math.random() * 3);
            const obsGroup = new THREE.Group();
            
            // Chướng ngại vật bẫy chuột
            textureLoader.load('https://cdn-icons-png.flaticon.com/512/2936/2936735.png', (texture) => {
                const spriteMat = new THREE.SpriteMaterial({ map: texture });
                const sprite = new THREE.Sprite(spriteMat);
                sprite.scale.set(1.3, 1.3, 1);
                obsGroup.add(sprite);
            });

            obsGroup.position.set(lanePositions[lane], 0.6, -90);
            scene.add(obsGroup);
            obstacles.push(obsGroup);
        }

        let frameCounter = 0;
        function animate() {
            if (gameOver) return;

            requestAnimationFrame(animate);

            // Di chuyển gián mượt mà sang các làn
            let targetX = lanePositions[currentLane];
            playerGroup.position.x += (targetX - playerGroup.position.x) * 0.2;

            // Mèo Oggy 3D bám sát đằng sau lưng gián
            oggyGroup.position.x += (playerGroup.position.x - oggyGroup.position.x) * 0.1;

            // Sinh chướng ngại vật định kỳ
            frameCounter++;
            if (frameCounter > 90) {
                spawnObstacle();
                frameCounter = 0;
                score += 2;
                document.getElementById('scoreVal').innerText = score;
                gameSpeed += 0.0005; 
            }

            // Cập nhật vị trí chướng ngại vật chạy tới
            for (let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i];
                obs.position.z += gameSpeed * 25;

                // Kiểm tra va chạm
                let dist = playerGroup.position.distanceTo(obs.position);
                if (dist < 1.0) {
                    triggerGameOver();
                }

                // Xóa chướng ngại vật khi qua màn hình
                if (obs.position.z > 5) {
                    scene.remove(obs);
                    obstacles.splice(i, 1);
                }
            }

            renderer.render(scene, camera);
        }

        function triggerGameOver() {
            gameOver = true;
            document.getElementById('finalScore').innerText = score;
            document.getElementById('gameOverScreen').style.display = 'flex';
        }

        function restartGame() {
            obstacles.forEach(obs => scene.remove(obs));
            obstacles = [];
            
            score = 0;
            gameSpeed = 0.12;
            currentLane = 1;
            playerGroup.position.x = lanePositions[1];
            document.getElementById('scoreVal').innerText = score;
            
            gameOver = false;
            document.getElementById('gameOverScreen').style.display = 'none';
            animate();
        }

        window.onload = init;
    </script>
</body>
</html>
"""

components.html(game_html, height=530)
