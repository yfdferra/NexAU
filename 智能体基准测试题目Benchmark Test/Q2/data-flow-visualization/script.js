// 2.5D等距视角数据流程可视化
// 使用Three.js创建等距视角的2.5D场景

// 场景、相机和渲染器
let scene, camera, renderer;
let dataFlowLines = [];
let animationFrameId;

// 等距视角参数
const ISOMETRIC_ANGLE = 30; // 等距视角角度
const CAMERA_DISTANCE = 1000; // 相机距离
const CAMERA_HEIGHT = 500; // 相机高度

// 节点位置参数
const NODE_SPACING = 200;
const NODE_Y_POSITION = 0;

// 初始化Three.js场景
function init() {
    // 创建场景
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a1a); // 深蓝色背景
    
    // 创建等距视角相机
    camera = new THREE.OrthographicCamera(
        window.innerWidth / -2,
        window.innerWidth / 2,
        window.innerHeight / 2,
        window.innerHeight / -2,
        1,
        10000
    );
    
    // 设置等距视角相机位置
    camera.position.set(500, 500, 500);
    camera.lookAt(0, 0, 0);
    
    // 创建渲染器
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.getElementById('scene-container').appendChild(renderer.domElement);
    
    // 添加光源
    addLights();
    
    // 创建2.5D等距场景
    createIsometricScene();
    
    // 创建数据流程节点
    createDataFlowNodes();
    
    // 创建数据流向连接线
    createDataFlowConnections();
    
    // 添加网格背景
    createGridBackground();
    
    // 开始动画
    animate();
    
    // 窗口大小调整事件
    window.addEventListener('resize', onWindowResize);
}

// 添加光源
function addLights() {
    // 环境光
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);
    
    // 方向光
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(100, 200, 100);
    scene.add(directionalLight);
    
    // 点光源用于发光效果
    const pointLight = new THREE.PointLight(0x4a90e2, 1, 1000);
    pointLight.position.set(0, 100, 0);
    scene.add(pointLight);
}

// 创建2.5D等距场景
function createIsometricScene() {
    // 创建地面平面
    const groundGeometry = new THREE.PlaneGeometry(2000, 1000);
    const groundMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x0a0a2a,
        transparent: true,
        opacity: 0.3
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -10;
    scene.add(ground);
}

// 创建数据流程节点
function createDataFlowNodes() {
    // 节点位置数组
    const nodePositions = [
        { x: -400, z: 0, label: "数据上链", data: "466.23", growth: "13.32%" },
        { x: -200, z: 0, label: "数据归集", data: null, growth: null },
        { x: 0, z: 100, label: "数据治理", data: null, growth: null },
        { x: 200, z: 0, label: "数据应用", data: "345.4", growth: "38.32%" },
        { x: 400, z: 0, label: "数据归档", data: "366.23", growth: "52.32%" }
    ];
    
    // 创建每个节点
    nodePositions.forEach((pos, index) => {
        createNode(pos.x, pos.z, pos.label, pos.data, pos.growth, index);
    });
}

// 创建单个节点
function createNode(x, z, label, data, growth, index) {
    let geometry, material, mesh;
    
    switch(index) {
        case 0: // 数据上链 - 高楼建筑
            geometry = new THREE.BoxGeometry(60, 120, 60);
            material = new THREE.MeshPhongMaterial({ 
                color: 0x1a5fb4,
                emissive: 0x0a3a7a,
                emissiveIntensity: 0.3,
                shininess: 100
            });
            mesh = new THREE.Mesh(geometry, material);
            
            // 添加顶部立方体
            const topCubeGeometry = new THREE.BoxGeometry(30, 30, 30);
            const topCubeMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x4a90e2,
                emissive: 0x1a5fb4,
                emissiveIntensity: 0.5
            });
            const topCube = new THREE.Mesh(topCubeGeometry, topCubeMaterial);
            topCube.position.y = 75;
            mesh.add(topCube);
            break;
            
        case 1: // 数据归集 - 处理节点
            geometry = new THREE.CylinderGeometry(40, 40, 80, 8);
            material = new THREE.MeshPhongMaterial({ 
                color: 0x2a7ad4,
                emissive: 0x0a5a9a,
                emissiveIntensity: 0.2
            });
            mesh = new THREE.Mesh(geometry, material);
            break;
            
        case 2: // 数据治理 - 服务器集群
            // 创建多个服务器模块
            const serverGroup = new THREE.Group();
            
            for(let i = 0; i < 4; i++) {
                const serverGeometry = new THREE.BoxGeometry(30, 40, 30);
                const serverMaterial = new THREE.MeshPhongMaterial({ 
                    color: 0x3a8ae4,
                    emissive: 0x1a6ac4,
                    emissiveIntensity: 0.3
                });
                const server = new THREE.Mesh(serverGeometry, serverMaterial);
                server.position.set(
                    (i % 2) * 40 - 20,
                    Math.floor(i / 2) * 50,
                    (i % 2) * 40 - 20
                );
                serverGroup.add(server);
            }
            
            mesh = serverGroup;
            break;
            
        case 3: // 数据应用 - 悬浮立方体
            geometry = new THREE.BoxGeometry(70, 70, 70);
            material = new THREE.MeshPhongMaterial({ 
                color: 0x5aa0f4,
                transparent: true,
                opacity: 0.7,
                emissive: 0x2a80d4,
                emissiveIntensity: 0.4
            });
            mesh = new THREE.Mesh(geometry, material);
            
            // 添加下方建筑
            const buildingGeometry = new THREE.BoxGeometry(50, 60, 50);
            const buildingMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x3a8ae4
            });
            const building = new THREE.Mesh(buildingGeometry, buildingMaterial);
            building.position.y = -65;
            mesh.add(building);
            break;
            
        case 4: // 数据归档 - 机器人
            // 创建机器人身体
            const bodyGeometry = new THREE.BoxGeometry(50, 70, 40);
            const bodyMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x4a90e2,
                emissive: 0x2a70c2,
                emissiveIntensity: 0.3
            });
            const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
            
            // 创建机器人头部
            const headGeometry = new THREE.SphereGeometry(20, 16, 16);
            const headMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x5aa0f2
            });
            const head = new THREE.Mesh(headGeometry, headMaterial);
            head.position.y = 45;
            body.add(head);
            
            // 创建机器人手臂
            const armGeometry = new THREE.BoxGeometry(10, 40, 10);
            const armMaterial = new THREE.MeshPhongMaterial({ 
                color: 0x3a80d2
            });
            
            const leftArm = new THREE.Mesh(armGeometry, armMaterial);
            leftArm.position.set(-30, 10, 0);
            body.add(leftArm);
            
            const rightArm = new THREE.Mesh(armGeometry, armMaterial);
            rightArm.position.set(30, 10, 0);
            body.add(rightArm);
            
            mesh = body;
            break;
    }
    
    mesh.position.set(x, NODE_Y_POSITION, z);
    scene.add(mesh);
    
    // 创建标签和数据展示
    if(data && growth) {
        createDataLabel(x, z + 80, label, data, growth);
    }
}

// 创建数据标签
function createDataLabel(x, z, label, data, growth) {
    // 创建HTML标签容器
    const labelContainer = document.createElement('div');
    labelContainer.className = 'data-label';
    labelContainer.style.position = 'absolute';
    labelContainer.style.color = '#ffffff';
    labelContainer.style.fontFamily = 'Arial, sans-serif';
    labelContainer.style.fontSize = '14px';
    labelContainer.style.textAlign = 'center';
    labelContainer.style.background = 'rgba(10, 20, 40, 0.8)';
    labelContainer.style.padding = '8px 12px';
    labelContainer.style.borderRadius = '4px';
    labelContainer.style.border = '1px solid rgba(74, 144, 226, 0.5)';
    labelContainer.style.boxShadow = '0 0 10px rgba(74, 144, 226, 0.3)';
    
    labelContainer.innerHTML = `
        <div style="font-weight: bold; margin-bottom: 4px;">${label}</div>
        <div style="font-size: 16px; color: #4a90e2; margin-bottom: 2px;">${data}</div>
        <div style="font-size: 12px; color: #ffcc00;">↑ ${growth}</div>
    `;
    
    document.getElementById('scene-container').appendChild(labelContainer);
    
    // 更新标签位置函数
    function updateLabelPosition() {
        const vector = new THREE.Vector3(x, NODE_Y_POSITION + 50, z);
        vector.project(camera);
        
        const xPos = (vector.x * 0.5 + 0.5) * window.innerWidth;
        const yPos = (-(vector.y * 0.5) + 0.5) * window.innerHeight;
        
        labelContainer.style.left = `${xPos - labelContainer.offsetWidth / 2}px`;
        labelContainer.style.top = `${yPos}px`;
    }
    
    // 在动画循环中更新位置
    const updateFunction = updateLabelPosition;
    dataFlowLines.push({ update: updateFunction });
}

// 创建数据流向连接线
function createDataFlowConnections() {
    // 连接线路径
    const connections = [
        { from: { x: -400, z: 0 }, to: { x: -200, z: 0 } },
        { from: { x: -200, z: 0 }, to: { x: 0, z: 100 } },
        { from: { x: 0, z: 100 }, to: { x: 200, z: 0 } },
        { from: { x: 200, z: 0 }, to: { x: 400, z: 0 } }
    ];
    
    connections.forEach(conn => {
        createFlowLine(conn.from, conn.to);
    });
}

// 创建流动的连接线
function createFlowLine(from, to) {
    // 创建曲线路径
    const curve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(from.x, NODE_Y_POSITION + 20, from.z),
        new THREE.Vector3((from.x + to.x) / 2, NODE_Y_POSITION + 40, (from.z + to.z) / 2),
        new THREE.Vector3(to.x, NODE_Y_POSITION + 20, to.z)
    ]);
    
    // 创建管状几何体
    const tubeGeometry = new THREE.TubeGeometry(curve, 20, 3, 8, false);
    const tubeMaterial = new THREE.MeshPhongMaterial({
        color: 0xffcc00,
        emissive: 0xff9900,
        emissiveIntensity: 0.5,
        transparent: true,
        opacity: 0.8
    });
    
    const tube = new THREE.Mesh(tubeGeometry, tubeMaterial);
    scene.add(tube);
    
    // 创建流动的光点
    const points = curve.getPoints(50);
    const flowPoints = [];
    
    for(let i = 0; i < 5; i++) {
        const sphereGeometry = new THREE.SphereGeometry(2, 8, 8);
        const sphereMaterial = new THREE.MeshBasicMaterial({
            color: 0xffff00,
            transparent: true,
            opacity: 0.8
        });
        
        const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
        scene.add(sphere);
        flowPoints.push({
            mesh: sphere,
            progress: i / 5,
            speed: 0.005 + Math.random() * 0.005
        });
    }
    
    // 添加到数据流线数组
    dataFlowLines.push({
        tube: tube,
        curve: curve,
        points: flowPoints,
        update: function(time) {
            // 更新流动光点位置
            this.points.forEach(point => {
                point.progress += point.speed;
                if(point.progress > 1) point.progress = 0;
                
                const position = this.curve.getPointAt(point.progress);
                point.mesh.position.copy(position);
                
                // 添加脉动效果
                const scale = 1 + 0.3 * Math.sin(time * 0.005 + point.progress * Math.PI * 2);
                point.mesh.scale.setScalar(scale);
            });
            
            // 更新管道发光效果
            const intensity = 0.5 + 0.3 * Math.sin(time * 0.002);
            this.tube.material.emissiveIntensity = intensity;
        }
    });
}

// 创建网格背景
function createGridBackground() {
    const gridHelper = new THREE.GridHelper(2000, 100, 0x1a3a7a, 0x0a2a5a);
    gridHelper.position.y = -5;
    scene.add(gridHelper);
}

// 动画循环
function animate() {
    animationFrameId = requestAnimationFrame(animate);
    
    const time = Date.now();
    
    // 更新数据流线
    dataFlowLines.forEach(line => {
        if(line.update) {
            if(line.tube) {
                line.update(time);
            } else if(typeof line.update === 'function') {
                line.update();
            }
        }
    });
    
    // 轻微旋转场景以获得更好的等距视角
    scene.rotation.y = time * 0.00005;
    
    renderer.render(scene, camera);
}

// 窗口大小调整处理
function onWindowResize() {
    camera.left = window.innerWidth / -2;
    camera.right = window.innerWidth / 2;
    camera.top = window.innerHeight / 2;
    camera.bottom = window.innerHeight / -2;
    camera.updateProjectionMatrix();
    
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// 初始化场景
init();