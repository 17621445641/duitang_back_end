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

 Date: 30/05/2022 19:27:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for update_code
-- ----------------------------
DROP TABLE IF EXISTS `update_code`;
CREATE TABLE `update_code`  (
  `user_id` int NULL DEFAULT NULL,
  `update_code` bigint NULL DEFAULT NULL,
  `create_time` datetime NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of update_code
-- ----------------------------
INSERT INTO `update_code` VALUES (1, 910262, '2022-05-30 01:24:08');

SET FOREIGN_KEY_CHECKS = 1;
