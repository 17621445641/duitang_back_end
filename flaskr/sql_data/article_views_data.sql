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

 Date: 02/06/2022 18:29:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article_views
-- ----------------------------
DROP TABLE IF EXISTS `article_views`;
CREATE TABLE `article_views`  (
  `user_id` int NULL DEFAULT NULL,
  `article_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `view_count` bigint NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `article_id`(`article_id`) USING BTREE,
  CONSTRAINT `article_views_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_message` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `article_views_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of article_views
-- ----------------------------
INSERT INTO `article_views` VALUES (NULL, '20200602958741', 6, '2022-06-02 02:13:56', '2022-06-02 02:14:48');
INSERT INTO `article_views` VALUES (1, '20200602152462', 2, '2022-06-02 02:41:00', '2022-06-02 02:41:10');
INSERT INTO `article_views` VALUES (1, '20200602145784', 1, '2022-06-02 02:41:22', '2022-06-02 02:41:22');

SET FOREIGN_KEY_CHECKS = 1;
