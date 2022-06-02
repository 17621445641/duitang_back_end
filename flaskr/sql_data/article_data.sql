/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80029
 Source Host           : localhost:3306
 Source Schema         : myproject

 Target Server Type    : MySQL
 Target Server Version : 80029
 File Encoding         : 65001

 Date: 02/06/2022 18:28:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article`  (
  `id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `article_title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `author_id` int NOT NULL,
  `article_content` varchar(20000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `view_status` int NULL DEFAULT NULL COMMENT '0仅自己可见，1公开',
  `create_time` datetime NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `author_id`(`author_id`) USING BTREE,
  CONSTRAINT `article_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user_message` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of article
-- ----------------------------
INSERT INTO `article` VALUES ('20200602145784', '雨巷', 1, '独自彷徨在悠长悠长又寂寥的雨巷', 1, '2022-06-02 10:07:46', '2022-06-02 10:07:49');
INSERT INTO `article` VALUES ('20200602152462', '静夜思', 2, '床前明月光，疑是地上霜', 1, '2022-06-02 10:07:46', '2022-06-02 10:07:49');
INSERT INTO `article` VALUES ('20200602958741', '登高', 2, '无边落木萧萧下，不尽长江滚滚来', 1, '2022-06-02 10:07:46', '2022-06-02 10:07:49');

SET FOREIGN_KEY_CHECKS = 1;
