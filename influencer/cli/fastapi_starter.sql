/*
 Navicat Premium Data Transfer

 Source Server         : local-mysql
 Source Server Type    : MySQL
 Source Server Version : 80300 (8.3.0)
 Source Host           : localhost:3306
 Source Schema         : fastapi_starter

 Target Server Type    : MySQL
 Target Server Version : 80300 (8.3.0)
 File Encoding         : 65001

 Date: 04/05/2024 02:07:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for system_admin
-- ----------------------------
DROP TABLE IF EXISTS `system_admin`;
CREATE TABLE `system_admin`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `is_super` tinyint NOT NULL DEFAULT 0 COMMENT '超级管理员 True:超级管理员 False:普通管理员',
  `role_ids` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '角色IDs',
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户账号',
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户密码',
  `real_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '真实姓名',
  `mobile` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户电话',
  `nickname` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户昵称',
  `avatar` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '头像',
  `gender` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '用户性别: [0=保密，1=男, 2=女]',
  `status` tinyint UNSIGNED NOT NULL DEFAULT 1 COMMENT '是否禁用: [0=停用, 1=正常]',
  `is_deleted` tinyint NULL DEFAULT 0 COMMENT '是否删除: [0=正常, 1=删除]',
  `create_time` TIMESTAMP NULL DEFAULT NOW() COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_admin
-- ----------------------------
INSERT INTO `system_admin` VALUES (1, 1, '', 'admin', '$2b$12$jY.imRvCVnzHT7.8RjrCU.S8U34oGQRBe4ySvbjvhNo5e0KEl7a3u', '', '', '超级', '', 0, 1, 0, '2022-03-31 11:18:15', '2022-03-31 11:18:15');

-- ----------------------------
-- Table structure for system_dept
-- ----------------------------
DROP TABLE IF EXISTS `system_dept`;
CREATE TABLE `system_dept`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '上级主键',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '部门名称',
  `leader` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '负责人名',
  `mobile` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '联系电话',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `sort` smallint UNSIGNED NOT NULL DEFAULT 0 COMMENT '排序编号',
  `status` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '状态: [0=停用, 1=正常]',
  `is_deleted` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否删除: [0=正常, 1=删除]',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统部门管理表' ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for system_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_menu`;
CREATE TABLE `system_menu`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '上级菜单',
  `menu_type` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '权限类型: M=目录，C=菜单，A=按钮',
  `menu_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '菜单名称',
  `menu_icon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '菜单图标',
  `sort` smallint UNSIGNED NOT NULL DEFAULT 0 COMMENT '菜单排序',
  `scopes` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '权限标识',
  `paths` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '路由地址',
  `component` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '前端组件',
  `params` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '路由参数',
  `is_cache` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否缓存: 0=否, 1=是',
  `is_show` tinyint UNSIGNED NOT NULL DEFAULT 1 COMMENT '是否显示: 0=否, 1=是',
  `status` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '状态: [0=停用, 1=正常]',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 777 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统菜单管理表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_menu
-- ----------------------------
INSERT INTO `system_menu` VALUES (1, 0, 'C', '工作台', 'el-icon-Monitor', 10, 'index:console', 'workbench', 'workbench/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2024-03-30 23:53:00');
INSERT INTO `system_menu` VALUES (100, 0, 'M', '系统管理', 'el-icon-Lock', 100, '', 'system', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (101, 100, 'C', '管理员', 'local-icon-wode', 0, 'system:admin:list', 'admin', 'system/admin/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (102, 101, 'A', '管理员详情', '', 0, 'system:admin:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (103, 101, 'A', '管理员新增', '', 0, 'system:admin:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (104, 101, 'A', '管理员编辑', '', 0, 'system:admin:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (105, 101, 'A', '管理员删除', '', 0, 'system:admin:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (106, 101, 'A', '管理员状态', '', 0, 'system:admin:disable', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (110, 100, 'C', '角色管理', 'el-icon-Female', 0, 'system:role:list', 'role', 'permission/role/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (111, 110, 'A', '角色详情', '', 0, 'system:role:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (112, 110, 'A', '角色新增', '', 0, 'system:role:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (113, 110, 'A', '角色编辑', '', 0, 'system:role:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (114, 110, 'A', '角色删除', '', 0, 'system:role:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (120, 100, 'C', '菜单管理', 'el-icon-Operation', 0, 'system:menu:list', 'menu', 'permission/menu/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (121, 120, 'A', '菜单详情', '', 0, 'system:menu:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (122, 120, 'A', '菜单新增', '', 0, 'system:menu:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (123, 120, 'A', '菜单编辑', '', 0, 'system:menu:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (124, 120, 'A', '菜单删除', '', 0, 'system:menu:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (131, 100, 'C', '部门管理', 'el-icon-Coordinate', 0, 'system:dept:list', 'department', 'organization/department/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (132, 131, 'A', '部门详情', '', 0, 'system:dept:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (133, 131, 'A', '部门新增', '', 0, 'system:dept:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (134, 131, 'A', '部门编辑', '', 0, 'system:dept:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (135, 131, 'A', '部门删除', '', 0, 'system:dept:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (140, 100, 'C', '岗位管理', 'el-icon-PriceTag', 0, 'system:post:list', 'post', 'organization/post/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (141, 140, 'A', '岗位详情', '', 0, 'system:post:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (142, 140, 'A', '岗位新增', '', 0, 'system:post:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (143, 140, 'A', '岗位编辑', '', 0, 'system:post:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (144, 140, 'A', '岗位删除', '', 0, 'system:post:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (700, 0, 'M', '云盘管理', 'el-icon-Picture', 70, '', 'dirver', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (701, 700, 'C', '网络云盘', 'el-icon-PictureRounded', 0, 'dirver', 'dirver/index', 'dirver/index', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (703, 0, 'M', '文章资讯', 'el-icon-ChatLineSquare', 49, '', 'article', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (704, 703, 'C', '文章管理', 'el-icon-ChatDotSquare', 3, 'article:list', 'lists', 'article/lists/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (705, 703, 'C', '文章栏目', 'el-icon-CollectionTag', 0, 'article:cate:list', 'column', 'article/column/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (712, 0, 'M', '用户管理', 'el-icon-User', 48, '', 'consumer', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (713, 712, 'C', '用户列表', 'el-icon-User', 0, 'user:list', 'lists', 'consumer/lists/index', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (714, 714, 'A', '用户编辑', '', 0, 'user:edit', 'detail', 'consumer/lists/detail', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (716, 705, 'A', '栏目详情', '', 0, 'article:cate:detail', 'lists/edit', 'article/lists/edit', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (730, 704, 'A', '文章新增', '', 0, 'article:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (732, 704, 'A', '文章删除', '', 0, 'article:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (733, 704, 'A', '文章状态', '', 0, 'article:change', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (734, 705, 'A', '栏目新增', '', 0, 'article:cate:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (735, 705, 'A', '栏目编辑', '', 0, 'article:cate:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (736, 705, 'A', '栏目删除', '', 0, 'article:cate:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (737, 705, 'A', '栏目状态', '', 0, 'article:cate:change', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (738, 704, 'A', '文章编辑', '', 0, 'article:edit', 'lists/edit', 'article/lists/edit', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (739, 712, 'C', '用户详情', '', 0, 'user:detail', 'detail', 'consumer/lists/detail', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (740, 739, 'A', '用户编辑', '', 0, 'user:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (755, 704, 'A', '文章详情', '', 0, 'article:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO `system_menu` VALUES (775, 703, 'C', '文章添加/编辑', '', 0, 'article:add/edit', 'lists/edit', 'article/lists/edit', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');

-- ----------------------------
-- Table structure for system_post
-- ----------------------------
DROP TABLE IF EXISTS `system_post`;
CREATE TABLE `system_post`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '岗位编码',
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '岗位名称',
  `remark` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '岗位备注',
  `sort` smallint UNSIGNED NOT NULL DEFAULT 0 COMMENT '岗位排序',
  `status` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '状态: [0=停用, 1=正常]',
  `is_deleted` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否删除: [0=正常, 1=删除]',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统岗位管理表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for system_role
-- ----------------------------
DROP TABLE IF EXISTS `system_role`;
CREATE TABLE `system_role`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '角色名称',
  `remark` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '备注信息',
  `sort` smallint UNSIGNED NOT NULL DEFAULT 0 COMMENT '角色排序',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '状态: [0=停用, 1=正常]',
  `is_deleted` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否删除: [0=正常, 1=删除]',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统角色管理表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for system_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_role_menu`;
CREATE TABLE `system_role_menu`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '角色ID',
  `menu_id` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '菜单ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 142 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统角色菜单表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for upload
-- ----------------------------
DROP TABLE IF EXISTS `upload`;
CREATE TABLE `upload`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `channel` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '上传来源（1 管理后台 2 Web端）',
  `folder_id` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '类目ID',
  `uid` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '用户ID（1管理后台admin，2web端user）',
  `type` tinyint UNSIGNED NOT NULL DEFAULT 10 COMMENT '文件类型: [10=图片, 20=视频，30=音频，40=文件]',
  `storage` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '存储位置',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '文件名称',
  `url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件路径',
  `ext` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '文件扩展',
  `size` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '文件大小',
  `is_deleted` tinyint NULL DEFAULT 0 COMMENT '是否删除: [0=正常, 1=删除]',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_cid`(`folder_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '相册管理表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for upload_folder
-- ----------------------------
DROP TABLE IF EXISTS `upload_folder`;
CREATE TABLE `upload_folder`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `pid` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '父级ID',
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '分类名称',
  `sort` int UNSIGNED NOT NULL DEFAULT 0 COMMENT '排序',
  `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '是否删除: [0=正常, 1=删除]',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '相册分类表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户账号',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户密码',
  `mobile` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户电话',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '邮箱',
  `nickname` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '用户昵称',
  `avatar` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '头像',
  `gender` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '用户性别: [0=保密，1=男, 2=女]',
  `intro` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '简介',
  `status` tinyint UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否禁用: [0=停用, 1=正常]',
  `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '是否删除: [0=正常, 1=删除]',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', '$2a$10$Ajkm/b4gw.eIm8HPXofPIesZJoRCe3NsVpWGkhKWc2gzraMdAy.Ci', '13800138000', '', '白白', '', 0, '', 0, 0, '2022-03-31 11:18:15', '2022-03-31 11:18:15');

SET FOREIGN_KEY_CHECKS = 1;
