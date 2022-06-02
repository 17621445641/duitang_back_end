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

 Date: 02/06/2022 18:29:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article_like
-- ----------------------------
DROP TABLE IF EXISTS `article_like`;
CREATE TABLE `article_like`  (
  `user_id` int NOT NULL,
  `article_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `like_status` int NOT NULL COMMENT '0,不喜欢，1喜欢',
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `article_id`(`article_id`) USING BTREE,
  CONSTRAINT `article_like_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_message` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `article_like_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of article_like
-- ----------------------------
INSERT INTO `article_like` VALUES (1, '20200602958741', 1, '2022-06-02 02:22:51', '2022-06-02 02:22:51');
INSERT INTO `article_like` VALUES (1, '20200602152462', 1, '2022-06-02 02:28:26', '2022-06-02 02:28:26');
INSERT INTO `article_like` VALUES (1, '20200602145784', 1, '2022-06-02 02:29:17', '2022-06-02 02:34:33');

SET FOREIGN_KEY_CHECKS = 1;
