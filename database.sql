-- 创建数据库表

-- 用户表
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    registration_date DATE DEFAULT CURRENT_DATE
);

-- WiFi型号表
CREATE TABLE IF NOT EXISTS WifiModel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    signalStrength REAL NOT NULL,
    speed REAL NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    rating REAL DEFAULT 0,
    reviewCount INTEGER DEFAULT 0
);

-- 数据套餐表
CREATE TABLE IF NOT EXISTS DataPlan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    wifiModelId INTEGER NOT NULL,
    FOREIGN KEY (wifiModelId) REFERENCES WifiModel(id) ON DELETE CASCADE
);

-- 评价表
CREATE TABLE IF NOT EXISTS Review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wifiModelId INTEGER NOT NULL,
    userId INTEGER NOT NULL,
    userName TEXT NOT NULL,
    rating REAL NOT NULL,
    comment TEXT,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (wifiModelId) REFERENCES WifiModel(id) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES User(id) ON DELETE CASCADE
);

-- 收藏表
CREATE TABLE IF NOT EXISTS Favorite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    wifiModelId INTEGER NOT NULL,
    FOREIGN KEY (userId) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (wifiModelId) REFERENCES WifiModel(id) ON DELETE CASCADE,
    UNIQUE(userId, wifiModelId)
);

-- 插入示例WiFi型号数据
INSERT INTO WifiModel (name, brand, model, signalStrength, speed, price, description, rating, reviewCount)
VALUES 
('华为随行WiFi 3', '华为', 'E5576-855', 4.5, 4.8, 299, '华为随行WiFi 3支持4G网络，最多可连接16台设备，续航时间长达8小时，适合旅行和办公使用。', 4.5, 125),
('小米移动WiFi', '小米', 'R1CL', 4.2, 4.5, 199, '小米移动WiFi采用简洁设计，支持4G网络，最多可连接10台设备，续航时间6小时，性价比高。', 4.2, 89),
('腾讯随身WiFi', '腾讯', 'Tencent WiFi', 3.8, 4.0, 129, '腾讯随身WiFi体积小巧，便于携带，支持4G网络，最多可连接8台设备，适合日常使用。', 3.9, 56),
('中兴MF920U', '中兴', 'MF920U', 4.6, 4.7, 349, '中兴MF920U支持4G+网络，最多可连接15台设备，续航时间长达10小时，信号稳定。', 4.6, 78),
('TP-Link M7350', 'TP-Link', 'M7350', 4.3, 4.4, 249, 'TP-Link M7350支持4G网络，最多可连接10台设备，续航时间8小时，操作简单。', 4.3, 67);

-- 插入示例数据套餐
INSERT INTO DataPlan (name, price, wifiModelId)
VALUES 
('月包10GB', 39, 1),
('月包20GB', 69, 1),
('月包50GB', 129, 1),
('月包5GB', 29, 2),
('月包15GB', 59, 2),
('月包30GB', 99, 2),
('月包3GB', 19, 3),
('月包10GB', 49, 3),
('月包20GB', 79, 3),
('月包15GB', 49, 4),
('月包30GB', 89, 4),
('月包60GB', 149, 4),
('月包8GB', 35, 5),
('月包20GB', 65, 5),
('月包40GB', 115, 5);
