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

 Date: 02/06/2022 18:30:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_avatar_image
-- ----------------------------
DROP TABLE IF EXISTS `user_avatar_image`;
CREATE TABLE `user_avatar_image`  (
  `user_id` int NULL DEFAULT NULL,
  `avatar_image_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT NULL,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `user_avatar_image_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_message` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_avatar_image
-- ----------------------------
INSERT INTO `user_avatar_image` VALUES (1, NULL, '2022-06-02 01:48:06');
INSERT INTO `user_avatar_image` VALUES (1, 'http://127.0.0.1:8998/static/avatar_images/dcbb4d20-dc4b-431a-8e13-d3db7d4d0e5f.jpeg', '2022-06-02 02:01:51');
INSERT INTO `user_avatar_image` VALUES (2, NULL, '2022-06-02 02:20:16');
INSERT INTO `user_avatar_image` VALUES (3, NULL, '2022-06-02 03:40:13');

SET FOREIGN_KEY_CHECKS = 1;
