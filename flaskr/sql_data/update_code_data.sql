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

 Date: 02/06/2022 18:30:05
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
  `create_time` datetime NULL DEFAULT NULL,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `update_code_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_message` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of update_code
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
