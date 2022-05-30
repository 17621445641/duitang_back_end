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

 Date: 30/05/2022 19:28:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for follow_history
-- ----------------------------
DROP TABLE IF EXISTS `follow_history`;
CREATE TABLE `follow_history`  (
  `follow_user_id` int NULL DEFAULT NULL,
  `be_follow_user_id` int NULL DEFAULT NULL,
  `follow_status` int NULL DEFAULT NULL COMMENT '0未关注，1已关注',
  `create_time` datetime NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of follow_history
-- ----------------------------
INSERT INTO `follow_history` VALUES (1, 2, 1, NULL, NULL);
INSERT INTO `follow_history` VALUES (5, 3, 1, NULL, NULL);
INSERT INTO `follow_history` VALUES (3, 1, 1, '2022-05-30 08:48:51', '2022-05-30 08:52:24');
INSERT INTO `follow_history` VALUES (8, 3, 1, '2022-05-17 19:06:03', '2022-05-25 19:06:06');
INSERT INTO `follow_history` VALUES (3, 8, 1, '2022-05-30 19:16:36', '2022-05-30 19:16:48');
INSERT INTO `follow_history` VALUES (3, 9, 1, '2022-05-30 11:22:19', '2022-05-30 11:23:09');
INSERT INTO `follow_history` VALUES (9, 3, 1, '2022-05-11 19:23:37', '2022-05-31 19:23:41');

SET FOREIGN_KEY_CHECKS = 1;
