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

 Date: 02/06/2022 18:29:52
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
  `update_time` datetime NULL DEFAULT NULL,
  INDEX `follow_user_id`(`follow_user_id`) USING BTREE,
  INDEX `be_follow_user_id`(`be_follow_user_id`) USING BTREE,
  CONSTRAINT `follow_history_ibfk_1` FOREIGN KEY (`follow_user_id`) REFERENCES `user_message` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `follow_history_ibfk_2` FOREIGN KEY (`be_follow_user_id`) REFERENCES `user_message` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of follow_history
-- ----------------------------
INSERT INTO `follow_history` VALUES (1, 2, 1, '2022-06-02 02:42:19', '2022-06-03 02:42:19');
INSERT INTO `follow_history` VALUES (1, 3, 0, '2022-06-02 03:40:28', '2022-06-02 03:40:28');
INSERT INTO `follow_history` VALUES (2, 1, 1, '2022-06-02 05:49:14', '2022-06-02 05:49:14');
INSERT INTO `follow_history` VALUES (3, 1, 1, '2022-06-02 13:55:33', '2022-06-02 13:55:37');

SET FOREIGN_KEY_CHECKS = 1;
