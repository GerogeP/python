/*
 Navicat Premium Data Transfer

 Source Server         : ifc_dev
 Source Server Type    : PostgreSQL
 Source Server Version : 140011 (140011)
 Source Host           : pgm-wz9v1k209z920er63o.pg.rds.aliyuncs.com:5532
 Source Catalog        : influencer_dev
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 140011 (140011)
 File Encoding         : 65001

 Date: 06/05/2024 10:49:55
*/


-- ----------------------------
-- Type structure for vector
-- ----------------------------
DROP TYPE IF EXISTS "public"."vector";
CREATE TYPE "public"."vector" (
  INPUT = "public"."vector_in",
  OUTPUT = "public"."vector_out",
  RECEIVE = "public"."vector_recv",
  SEND = "public"."vector_send",
  TYPMOD_IN = "public"."vector_typmod_in",
  INTERNALLENGTH = VARIABLE,
  STORAGE = external,
  CATEGORY = U,
  DELIMITER = ','
);
ALTER TYPE "public"."vector" OWNER TO "moaidev";

-- ----------------------------
-- Sequence structure for influencer_manual_tags_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."influencer_manual_tags_id_seq";
CREATE SEQUENCE "public"."influencer_manual_tags_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for influencer_param_histories_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."influencer_param_histories_id_seq";
CREATE SEQUENCE "public"."influencer_param_histories_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for influencers_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."influencers_id_seq";
CREATE SEQUENCE "public"."influencers_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for items_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."items_id_seq";
CREATE SEQUENCE "public"."items_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for msg_store_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."msg_store_id_seq";
CREATE SEQUENCE "public"."msg_store_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for msg_tasks_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."msg_tasks_id_seq";
CREATE SEQUENCE "public"."msg_tasks_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for new_msgs_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."new_msgs_id_seq";
CREATE SEQUENCE "public"."new_msgs_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for system_admin_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."system_admin_id_seq";
CREATE SEQUENCE "public"."system_admin_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for system_dept_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."system_dept_id_seq";
CREATE SEQUENCE "public"."system_dept_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for system_menu_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."system_menu_id_seq";
CREATE SEQUENCE "public"."system_menu_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for system_post_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."system_post_id_seq";
CREATE SEQUENCE "public"."system_post_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for system_role_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."system_role_id_seq";
CREATE SEQUENCE "public"."system_role_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for system_role_menu_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."system_role_menu_id_seq";
CREATE SEQUENCE "public"."system_role_menu_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for upload_folder_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."upload_folder_id_seq";
CREATE SEQUENCE "public"."upload_folder_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for upload_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."upload_id_seq";
CREATE SEQUENCE "public"."upload_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."user_id_seq";
CREATE SEQUENCE "public"."user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for workflow_params_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."workflow_params_id_seq";
CREATE SEQUENCE "public"."workflow_params_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for workflows_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."workflows_id_seq";
CREATE SEQUENCE "public"."workflows_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for influencer_manual_tags
-- ----------------------------
DROP TABLE IF EXISTS "public"."influencer_manual_tags";
CREATE TABLE "public"."influencer_manual_tags" (
  "id" int4 NOT NULL DEFAULT nextval('influencer_manual_tags_id_seq'::regclass),
  "influencer_id" int4,
  "tags" varchar(255)[] COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" timestamp(6)
)
;

-- ----------------------------
-- Records of influencer_manual_tags
-- ----------------------------

-- ----------------------------
-- Table structure for influencer_param_histories
-- ----------------------------
DROP TABLE IF EXISTS "public"."influencer_param_histories";
CREATE TABLE "public"."influencer_param_histories" (
  "id" int4 NOT NULL DEFAULT nextval('influencer_param_histories_id_seq'::regclass),
  "influencer_id" int4,
  "param" jsonb NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" timestamp(6)
)
;

-- ----------------------------
-- Records of influencer_param_histories
-- ----------------------------

-- ----------------------------
-- Table structure for influencers
-- ----------------------------
DROP TABLE IF EXISTS "public"."influencers";
CREATE TABLE "public"."influencers" (
  "id" int4 NOT NULL DEFAULT nextval('influencers_id_seq'::regclass),
  "site_id" varchar COLLATE "pg_catalog"."default",
  "influencer_account" varchar COLLATE "pg_catalog"."default",
  "param" jsonb NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" timestamp(6)
)
;

-- ----------------------------
-- Records of influencers
-- ----------------------------

-- ----------------------------
-- Table structure for items
-- ----------------------------
DROP TABLE IF EXISTS "public"."items";
CREATE TABLE "public"."items" (
  "id" int8 NOT NULL DEFAULT nextval('items_id_seq'::regclass),
  "embedding" "public"."vector"
)
;

-- ----------------------------
-- Records of items
-- ----------------------------
INSERT INTO "public"."items" VALUES (1, '[1,2,3]');
INSERT INTO "public"."items" VALUES (2, '[4,5,6]');

-- ----------------------------
-- Table structure for msg_store
-- ----------------------------
DROP TABLE IF EXISTS "public"."msg_store";
CREATE TABLE "public"."msg_store" (
  "id" int4 NOT NULL DEFAULT nextval('msg_store_id_seq'::regclass),
  "influencer_id" int4,
  "msg_list" jsonb NOT NULL,
  "msg_updated_at" timestamp(6) NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" timestamp(6),
  "affiliate_account" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of msg_store
-- ----------------------------

-- ----------------------------
-- Table structure for msg_tasks
-- ----------------------------
DROP TABLE IF EXISTS "public"."msg_tasks";
CREATE TABLE "public"."msg_tasks" (
  "id" int4 NOT NULL DEFAULT nextval('msg_tasks_id_seq'::regclass),
  "task_type" varchar COLLATE "pg_catalog"."default",
  "affiliate_account" varchar COLLATE "pg_catalog"."default",
  "influencer_id" int4,
  "state" varchar COLLATE "pg_catalog"."default",
  "msg_list" text[] COLLATE "pg_catalog"."default",
  "workflow_id" int4,
  "workflow_event" varchar COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" timestamp(6)
)
;

-- ----------------------------
-- Records of msg_tasks
-- ----------------------------

-- ----------------------------
-- Table structure for new_msgs
-- ----------------------------
DROP TABLE IF EXISTS "public"."new_msgs";
CREATE TABLE "public"."new_msgs" (
  "id" int4 NOT NULL DEFAULT nextval('new_msgs_id_seq'::regclass),
  "msg_store_id" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" timestamp(6)
)
;

-- ----------------------------
-- Records of new_msgs
-- ----------------------------

-- ----------------------------
-- Table structure for system_admin
-- ----------------------------
DROP TABLE IF EXISTS "public"."system_admin";
CREATE TABLE "public"."system_admin" (
  "id" int4 NOT NULL DEFAULT nextval('system_admin_id_seq'::regclass),
  "is_super" int2 NOT NULL,
  "role_ids" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "username" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "password" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "real_name" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "mobile" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "nickname" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "avatar" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "gender" int2 NOT NULL,
  "status" int2 NOT NULL,
  "is_deleted" int2,
  "create_time" timestamp(6) NOT NULL DEFAULT now(),
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."system_admin"."id" IS '主键';
COMMENT ON COLUMN "public"."system_admin"."is_super" IS '超级管理员 True:超级管理员 False:普通管理员';
COMMENT ON COLUMN "public"."system_admin"."role_ids" IS '角色IDs';
COMMENT ON COLUMN "public"."system_admin"."username" IS '用户账号';
COMMENT ON COLUMN "public"."system_admin"."password" IS '用户密码';
COMMENT ON COLUMN "public"."system_admin"."real_name" IS '真实姓名';
COMMENT ON COLUMN "public"."system_admin"."mobile" IS '用户电话';
COMMENT ON COLUMN "public"."system_admin"."nickname" IS '用户昵称';
COMMENT ON COLUMN "public"."system_admin"."avatar" IS '头像';
COMMENT ON COLUMN "public"."system_admin"."gender" IS '用户性别: [0=保密，1=男, 2=女]';
COMMENT ON COLUMN "public"."system_admin"."status" IS '是否禁用: [0=停用, 1=正常]';
COMMENT ON COLUMN "public"."system_admin"."is_deleted" IS '是否删除: [False=正常, True=删除]';
COMMENT ON COLUMN "public"."system_admin"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."system_admin"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."system_admin" IS '用户信息表';

-- ----------------------------
-- Records of system_admin
-- ----------------------------
INSERT INTO "public"."system_admin" VALUES (1, 1, '', 'admin', '$2b$12$jY.imRvCVnzHT7.8RjrCU.S8U34oGQRBe4ySvbjvhNo5e0KEl7a3u', '', '', '超级管理员', '', 0, 1, 0, '2022-03-31 11:18:15', '2022-03-31 11:18:15');
INSERT INTO "public"."system_admin" VALUES (2, 0, '1', 'pinhaibd', '$2b$12$4CL5ZHckw89aAX3UaIZsruDI0oq/0XlGu.rfE8dalF.pG2jHNYt2y', '品海BD', ' ', '品海BD', ' ', 0, 1, 0, '2024-05-05 22:41:49', '2024-05-05 22:41:51');
INSERT INTO "public"."system_admin" VALUES (3, 0, '3', 'test001', '$2b$12$1wTaxrc81gY19DvhmavtAeEnR80iSjHJTrHmQUYKeDmHy8io2lgLC', '', '', '测试用户', '', 0, 1, 0, '2024-05-06 10:23:03.416609', '2024-05-06 10:23:03.416609');

-- ----------------------------
-- Table structure for system_dept
-- ----------------------------
DROP TABLE IF EXISTS "public"."system_dept";
CREATE TABLE "public"."system_dept" (
  "id" int4 NOT NULL DEFAULT nextval('system_dept_id_seq'::regclass),
  "pid" int8 NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "leader" varchar(30) COLLATE "pg_catalog"."default",
  "mobile" varchar(30) COLLATE "pg_catalog"."default",
  "remark" varchar(255) COLLATE "pg_catalog"."default",
  "sort" int4 NOT NULL,
  "status" int2 NOT NULL,
  "is_deleted" int2 NOT NULL,
  "create_time" timestamp(6) NOT NULL DEFAULT now(),
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."system_dept"."id" IS '主键';
COMMENT ON COLUMN "public"."system_dept"."pid" IS '上级主键';
COMMENT ON COLUMN "public"."system_dept"."name" IS '部门名称';
COMMENT ON COLUMN "public"."system_dept"."leader" IS '负责人名';
COMMENT ON COLUMN "public"."system_dept"."mobile" IS '联系电话';
COMMENT ON COLUMN "public"."system_dept"."remark" IS '备注';
COMMENT ON COLUMN "public"."system_dept"."sort" IS '排序编号';
COMMENT ON COLUMN "public"."system_dept"."status" IS '状态: [0=停用, 1=正常]';
COMMENT ON COLUMN "public"."system_dept"."is_deleted" IS '是否删除: [False=正常, True=删除]';
COMMENT ON COLUMN "public"."system_dept"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."system_dept"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."system_dept" IS '系统部门管理表';

-- ----------------------------
-- Records of system_dept
-- ----------------------------
INSERT INTO "public"."system_dept" VALUES (1, 0, '默认部门', '康明', '18327647788', '', 10, 0, 0, '2024-03-13 02:08:06', '2024-03-27 02:08:10');
INSERT INTO "public"."system_dept" VALUES (10, 0, '测试部门', '小明', '13800138000', '', 1, 1, 0, '2024-03-31 02:18:28', '2024-03-31 02:18:28');
INSERT INTO "public"."system_dept" VALUES (11, 10, '123123', NULL, NULL, '', 1, 1, 0, '2024-03-31 02:21:14', '2024-03-31 02:21:14');
INSERT INTO "public"."system_dept" VALUES (12, 0, '技术IT', '', '', '', 1, 1, 0, '2024-05-01 23:35:14', '2024-05-01 23:35:14');

-- ----------------------------
-- Table structure for system_menu
-- ----------------------------
DROP TABLE IF EXISTS "public"."system_menu";
CREATE TABLE "public"."system_menu" (
  "id" int4 NOT NULL DEFAULT nextval('system_menu_id_seq'::regclass),
  "pid" int8 NOT NULL,
  "menu_type" char(2) COLLATE "pg_catalog"."default" NOT NULL,
  "menu_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "menu_icon" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "sort" int4 NOT NULL,
  "scopes" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "paths" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "component" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "params" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "is_cache" int2 NOT NULL,
  "is_show" int2 NOT NULL,
  "status" int2 NOT NULL,
  "create_time" timestamp(6) NOT NULL DEFAULT now(),
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."system_menu"."id" IS '主键';
COMMENT ON COLUMN "public"."system_menu"."pid" IS '上级菜单';
COMMENT ON COLUMN "public"."system_menu"."menu_type" IS '权限类型: M=目录，C=菜单，A=按钮';
COMMENT ON COLUMN "public"."system_menu"."menu_name" IS '菜单名称';
COMMENT ON COLUMN "public"."system_menu"."menu_icon" IS '菜单图标';
COMMENT ON COLUMN "public"."system_menu"."sort" IS '菜单排序';
COMMENT ON COLUMN "public"."system_menu"."scopes" IS '权限标识';
COMMENT ON COLUMN "public"."system_menu"."paths" IS '路由地址';
COMMENT ON COLUMN "public"."system_menu"."component" IS '前端组件';
COMMENT ON COLUMN "public"."system_menu"."params" IS '路由参数';
COMMENT ON COLUMN "public"."system_menu"."is_cache" IS '是否缓存: 0=否, 1=是';
COMMENT ON COLUMN "public"."system_menu"."is_show" IS '是否显示: 0=否, 1=是';
COMMENT ON COLUMN "public"."system_menu"."status" IS '状态: [0=停用, 1=正常]';
COMMENT ON COLUMN "public"."system_menu"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."system_menu"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."system_menu" IS '系统菜单管理表';

-- ----------------------------
-- Records of system_menu
-- ----------------------------
INSERT INTO "public"."system_menu" VALUES (111, 110, 'A ', '角色详情', '', 0, 'system:role:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (112, 110, 'A ', '角色新增', '', 0, 'system:role:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (113, 110, 'A ', '角色编辑', '', 0, 'system:role:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (114, 110, 'A ', '角色删除', '', 0, 'system:role:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (121, 120, 'A ', '菜单详情', '', 0, 'system:menu:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (122, 120, 'A ', '菜单新增', '', 0, 'system:menu:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (123, 120, 'A ', '菜单编辑', '', 0, 'system:menu:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (124, 120, 'A ', '菜单删除', '', 0, 'system:menu:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (132, 131, 'A ', '部门详情', '', 0, 'system:dept:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (133, 131, 'A ', '部门新增', '', 0, 'system:dept:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (134, 131, 'A ', '部门编辑', '', 0, 'system:dept:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (135, 131, 'A ', '部门删除', '', 0, 'system:dept:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (141, 140, 'A ', '岗位详情', '', 0, 'system:post:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (142, 140, 'A ', '岗位新增', '', 0, 'system:post:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (143, 140, 'A ', '岗位编辑', '', 0, 'system:post:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (144, 140, 'A ', '岗位删除', '', 0, 'system:post:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (700, 0, 'M ', '云盘管理', 'el-icon-Picture', 70, '', 'dirver', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (701, 700, 'C ', '网络云盘', 'el-icon-PictureRounded', 0, 'dirver', 'dirver/index', 'dirver/index', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (703, 0, 'M ', '文章资讯', 'el-icon-ChatLineSquare', 49, '', 'article', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (704, 703, 'C ', '文章管理', 'el-icon-ChatDotSquare', 3, 'article:list', 'lists', 'article/lists/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (705, 703, 'C ', '文章栏目', 'el-icon-CollectionTag', 0, 'article:cate:list', 'column', 'article/column/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (712, 0, 'M ', '用户管理', 'el-icon-User', 48, '', 'consumer', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (713, 712, 'C ', '用户列表', 'el-icon-User', 0, 'user:list', 'lists', 'consumer/lists/index', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (714, 714, 'A ', '用户编辑', '', 0, 'user:edit', 'detail', 'consumer/lists/detail', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (716, 705, 'A ', '栏目详情', '', 0, 'article:cate:detail', 'lists/edit', 'article/lists/edit', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (730, 704, 'A ', '文章新增', '', 0, 'article:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (732, 704, 'A ', '文章删除', '', 0, 'article:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (733, 704, 'A ', '文章状态', '', 0, 'article:change', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (734, 705, 'A ', '栏目新增', '', 0, 'article:cate:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (735, 705, 'A ', '栏目编辑', '', 0, 'article:cate:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (736, 705, 'A ', '栏目删除', '', 0, 'article:cate:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (737, 705, 'A ', '栏目状态', '', 0, 'article:cate:change', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (738, 704, 'A ', '文章编辑', '', 0, 'article:edit', 'lists/edit', 'article/lists/edit', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (739, 712, 'C ', '用户详情', '', 0, 'user:detail', 'detail', 'consumer/lists/detail', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (740, 739, 'A ', '用户编辑', '', 0, 'user:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (755, 704, 'A ', '文章详情', '', 0, 'article:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (775, 703, 'C ', '文章添加/编辑', '', 0, 'article:add/edit', 'lists/edit', 'article/lists/edit', '', 0, 0, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (1, 0, 'C ', '工作台', 'el-icon-Monitor', 10, 'index:console', 'workbench', 'workbench/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2024-03-30 23:53:00');
INSERT INTO "public"."system_menu" VALUES (100, 0, 'M ', '系统管理', 'el-icon-Lock', 100, '', 'system', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (101, 100, 'C ', '管理员', 'local-icon-wode', 0, 'system:admin:list', 'admin', 'system/admin/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (102, 101, 'A ', '管理员详情', '', 0, 'system:admin:detail', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (103, 101, 'A ', '管理员新增', '', 0, 'system:admin:add', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (104, 101, 'A ', '管理员编辑', '', 0, 'system:admin:edit', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (105, 101, 'A ', '管理员删除', '', 0, 'system:admin:del', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (106, 101, 'A ', '管理员状态', '', 0, 'system:admin:disable', '', '', '', 0, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (120, 100, 'C ', '菜单管理', 'el-icon-Operation', 2, 'system:menu:list', 'menu', 'permission/menu/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (110, 100, 'C ', '角色管理', 'el-icon-Female', 1, 'system:role:list', 'role', 'permission/role/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (131, 100, 'C ', '部门管理', 'el-icon-Coordinate', 3, 'system:dept:list', 'department', 'organization/department/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');
INSERT INTO "public"."system_menu" VALUES (140, 100, 'C ', '岗位管理', 'el-icon-PriceTag', 4, 'system:post:list', 'post', 'organization/post/index', '', 1, 1, 1, '2022-01-01 12:13:14', '2022-01-01 12:13:14');

-- ----------------------------
-- Table structure for system_post
-- ----------------------------
DROP TABLE IF EXISTS "public"."system_post";
CREATE TABLE "public"."system_post" (
  "id" int4 NOT NULL DEFAULT nextval('system_post_id_seq'::regclass),
  "code" varchar(30) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(30) COLLATE "pg_catalog"."default" NOT NULL,
  "remark" varchar(250) COLLATE "pg_catalog"."default" NOT NULL,
  "sort" int4 NOT NULL,
  "status" int2 NOT NULL,
  "is_deleted" int2 NOT NULL,
  "create_time" timestamp(6) NOT NULL DEFAULT now(),
  "update_time" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."system_post"."id" IS '主键';
COMMENT ON COLUMN "public"."system_post"."code" IS '岗位编码';
COMMENT ON COLUMN "public"."system_post"."name" IS '岗位名称';
COMMENT ON COLUMN "public"."system_post"."remark" IS '岗位备注';
COMMENT ON COLUMN "public"."system_post"."sort" IS '岗位排序';
COMMENT ON COLUMN "public"."system_post"."status" IS '状态: [0=停用, 1=正常]';
COMMENT ON COLUMN "public"."system_post"."is_deleted" IS '是否删除: [False=正常, True=删除]';
COMMENT ON COLUMN "public"."system_post"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."system_post"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."system_post" IS '系统岗位管理表';

-- ----------------------------
-- Records of system_post
-- ----------------------------
INSERT INTO "public"."system_post" VALUES (1, 'Develop', '产品研发', '', 1, 1, 0, '2024-05-06 10:37:15.327776', '2024-05-06 10:37:15.327776');
INSERT INTO "public"."system_post" VALUES (2, 'Test', '测试', '产品测试', 1, 1, 0, '2024-05-06 10:37:43.407774', '2024-05-06 10:37:43.407774');

-- ----------------------------
-- Table structure for system_role
-- ----------------------------
DROP TABLE IF EXISTS "public"."system_role";
CREATE TABLE "public"."system_role" (
  "id" int4 NOT NULL DEFAULT nextval('system_role_id_seq'::regclass),
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "remark" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "sort" int4 NOT NULL,
  "status" int2 NOT NULL,
  "is_deleted" int2 NOT NULL,
  "create_time" timestamptz(6) NOT NULL DEFAULT now(),
  "update_time" timestamptz(6) NOT NULL DEFAULT now()
)
;
COMMENT ON COLUMN "public"."system_role"."id" IS '主键';
COMMENT ON COLUMN "public"."system_role"."name" IS '角色名称';
COMMENT ON COLUMN "public"."system_role"."remark" IS '备注信息';
COMMENT ON COLUMN "public"."system_role"."sort" IS '角色排序';
COMMENT ON COLUMN "public"."system_role"."status" IS '状态: [0=停用, 1=正常]';
COMMENT ON COLUMN "public"."system_role"."is_deleted" IS '是否删除: [False=正常, True=删除]';
COMMENT ON COLUMN "public"."system_role"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."system_role"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."system_role" IS '系统角色管理表';

-- ----------------------------
-- Records of system_role
-- ----------------------------
INSERT INTO "public"."system_role" VALUES (3, 'BD', '', 1, 1, 0, '2024-05-06 10:46:42.645461+08', '2024-05-06 10:46:42.645461+08');

-- ----------------------------
-- Table structure for system_role_menu
-- ----------------------------
DROP TABLE IF EXISTS "public"."system_role_menu";
CREATE TABLE "public"."system_role_menu" (
  "id" int4 NOT NULL DEFAULT nextval('system_role_menu_id_seq'::regclass),
  "role_id" int8,
  "menu_id" int8
)
;

-- ----------------------------
-- Records of system_role_menu
-- ----------------------------
INSERT INTO "public"."system_role_menu" VALUES (1, 1, 1);
INSERT INTO "public"."system_role_menu" VALUES (2, 4, 1);
INSERT INTO "public"."system_role_menu" VALUES (3, 4, 712);
INSERT INTO "public"."system_role_menu" VALUES (4, 4, 739);
INSERT INTO "public"."system_role_menu" VALUES (5, 4, 740);
INSERT INTO "public"."system_role_menu" VALUES (6, 4, 713);
INSERT INTO "public"."system_role_menu" VALUES (7, 4, 703);
INSERT INTO "public"."system_role_menu" VALUES (8, 4, 775);
INSERT INTO "public"."system_role_menu" VALUES (9, 4, 705);
INSERT INTO "public"."system_role_menu" VALUES (10, 4, 716);
INSERT INTO "public"."system_role_menu" VALUES (11, 4, 734);
INSERT INTO "public"."system_role_menu" VALUES (12, 4, 735);
INSERT INTO "public"."system_role_menu" VALUES (13, 4, 736);
INSERT INTO "public"."system_role_menu" VALUES (14, 4, 737);
INSERT INTO "public"."system_role_menu" VALUES (15, 4, 704);
INSERT INTO "public"."system_role_menu" VALUES (16, 4, 755);
INSERT INTO "public"."system_role_menu" VALUES (17, 4, 730);
INSERT INTO "public"."system_role_menu" VALUES (18, 4, 732);
INSERT INTO "public"."system_role_menu" VALUES (19, 4, 733);
INSERT INTO "public"."system_role_menu" VALUES (20, 4, 738);
INSERT INTO "public"."system_role_menu" VALUES (21, 4, 700);
INSERT INTO "public"."system_role_menu" VALUES (22, 4, 701);
INSERT INTO "public"."system_role_menu" VALUES (23, 4, 100);
INSERT INTO "public"."system_role_menu" VALUES (24, 4, 101);
INSERT INTO "public"."system_role_menu" VALUES (25, 4, 102);
INSERT INTO "public"."system_role_menu" VALUES (26, 4, 103);
INSERT INTO "public"."system_role_menu" VALUES (27, 4, 104);
INSERT INTO "public"."system_role_menu" VALUES (28, 4, 105);
INSERT INTO "public"."system_role_menu" VALUES (29, 4, 106);
INSERT INTO "public"."system_role_menu" VALUES (30, 4, 110);
INSERT INTO "public"."system_role_menu" VALUES (31, 4, 112);
INSERT INTO "public"."system_role_menu" VALUES (32, 4, 113);
INSERT INTO "public"."system_role_menu" VALUES (33, 4, 114);
INSERT INTO "public"."system_role_menu" VALUES (34, 4, 111);
INSERT INTO "public"."system_role_menu" VALUES (35, 4, 120);
INSERT INTO "public"."system_role_menu" VALUES (36, 4, 121);
INSERT INTO "public"."system_role_menu" VALUES (37, 4, 122);
INSERT INTO "public"."system_role_menu" VALUES (38, 4, 123);
INSERT INTO "public"."system_role_menu" VALUES (39, 4, 124);
INSERT INTO "public"."system_role_menu" VALUES (40, 4, 131);
INSERT INTO "public"."system_role_menu" VALUES (41, 4, 132);
INSERT INTO "public"."system_role_menu" VALUES (42, 4, 133);
INSERT INTO "public"."system_role_menu" VALUES (43, 4, 134);
INSERT INTO "public"."system_role_menu" VALUES (44, 4, 135);
INSERT INTO "public"."system_role_menu" VALUES (45, 4, 140);
INSERT INTO "public"."system_role_menu" VALUES (46, 4, 141);
INSERT INTO "public"."system_role_menu" VALUES (47, 4, 142);
INSERT INTO "public"."system_role_menu" VALUES (48, 4, 143);
INSERT INTO "public"."system_role_menu" VALUES (49, 4, 144);

-- ----------------------------
-- Table structure for upload
-- ----------------------------
DROP TABLE IF EXISTS "public"."upload";
CREATE TABLE "public"."upload" (
  "id" int4 NOT NULL DEFAULT nextval('upload_id_seq'::regclass),
  "channel" int8 NOT NULL,
  "folder_id" int8 NOT NULL,
  "uid" int8 NOT NULL,
  "type" int2 NOT NULL,
  "storage" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "url" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "ext" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "size" int8 NOT NULL,
  "is_deleted" int2,
  "create_time" timestamp(6) NOT NULL DEFAULT now(),
  "update_time" timestamp(6) NOT NULL DEFAULT now()
)
;
COMMENT ON COLUMN "public"."upload"."id" IS '主键ID';
COMMENT ON COLUMN "public"."upload"."channel" IS '上传来源（1 管理后台 2 Web端）';
COMMENT ON COLUMN "public"."upload"."folder_id" IS '类目ID';
COMMENT ON COLUMN "public"."upload"."uid" IS '用户ID（1管理后台admin，2web端user）';
COMMENT ON COLUMN "public"."upload"."type" IS '文件类型: [10=图片, 20=视频，30=音频，40=文件]';
COMMENT ON COLUMN "public"."upload"."storage" IS '存储位置';
COMMENT ON COLUMN "public"."upload"."name" IS '文件名称';
COMMENT ON COLUMN "public"."upload"."url" IS '文件路径';
COMMENT ON COLUMN "public"."upload"."ext" IS '文件扩展';
COMMENT ON COLUMN "public"."upload"."size" IS '文件大小';
COMMENT ON COLUMN "public"."upload"."is_deleted" IS '是否删除: [False=正常, True=删除]';
COMMENT ON COLUMN "public"."upload"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."upload"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."upload" IS '上传文件表';

-- ----------------------------
-- Records of upload
-- ----------------------------

-- ----------------------------
-- Table structure for upload_folder
-- ----------------------------
DROP TABLE IF EXISTS "public"."upload_folder";
CREATE TABLE "public"."upload_folder" (
  "id" int4 NOT NULL DEFAULT nextval('upload_folder_id_seq'::regclass),
  "pid" int8 NOT NULL,
  "name" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "sort" int8 NOT NULL,
  "is_deleted" int2 NOT NULL,
  "create_time" timestamp(6) NOT NULL DEFAULT now(),
  "update_time" timestamp(6) NOT NULL DEFAULT now()
)
;
COMMENT ON COLUMN "public"."upload_folder"."id" IS '主键ID';
COMMENT ON COLUMN "public"."upload_folder"."pid" IS '父级ID';
COMMENT ON COLUMN "public"."upload_folder"."name" IS '分类名称';
COMMENT ON COLUMN "public"."upload_folder"."sort" IS '排序';
COMMENT ON COLUMN "public"."upload_folder"."is_deleted" IS '是否删除: [False=正常, True=删除]';
COMMENT ON COLUMN "public"."upload_folder"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."upload_folder"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."upload_folder" IS '上传文件分类表';

-- ----------------------------
-- Records of upload_folder
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "public"."user";
CREATE TABLE "public"."user" (
  "id" int4 NOT NULL DEFAULT nextval('user_id_seq'::regclass),
  "username" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "password" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "mobile" varchar(11) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "nickname" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "avatar" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "gender" int2 NOT NULL,
  "intro" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "status" int2 NOT NULL,
  "is_deleted" int2 NOT NULL,
  "create_time" timestamp(6) NOT NULL DEFAULT now(),
  "update_time" timestamp(6) NOT NULL DEFAULT now()
)
;
COMMENT ON COLUMN "public"."user"."id" IS '主键';
COMMENT ON COLUMN "public"."user"."username" IS '用户账号';
COMMENT ON COLUMN "public"."user"."password" IS '用户密码';
COMMENT ON COLUMN "public"."user"."mobile" IS '用户电话';
COMMENT ON COLUMN "public"."user"."email" IS '邮箱';
COMMENT ON COLUMN "public"."user"."nickname" IS '用户昵称';
COMMENT ON COLUMN "public"."user"."avatar" IS '头像';
COMMENT ON COLUMN "public"."user"."gender" IS '用户性别: [0=保密，1=男, 2=女]';
COMMENT ON COLUMN "public"."user"."intro" IS '简介';
COMMENT ON COLUMN "public"."user"."status" IS '是否禁用: [0=停用, 1=正常]';
COMMENT ON COLUMN "public"."user"."is_deleted" IS '是否删除: [False=正常, True=删除]';
COMMENT ON COLUMN "public"."user"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."user"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."user" IS '用户信息表';

-- ----------------------------
-- Records of user
-- ----------------------------

-- ----------------------------
-- Table structure for workflow_params
-- ----------------------------
DROP TABLE IF EXISTS "public"."workflow_params";
CREATE TABLE "public"."workflow_params" (
  "id" int4 NOT NULL DEFAULT nextval('workflow_params_id_seq'::regclass),
  "param" jsonb NOT NULL
)
;

-- ----------------------------
-- Records of workflow_params
-- ----------------------------

-- ----------------------------
-- Table structure for workflows
-- ----------------------------
DROP TABLE IF EXISTS "public"."workflows";
CREATE TABLE "public"."workflows" (
  "id" int4 NOT NULL DEFAULT nextval('workflows_id_seq'::regclass),
  "template_id" varchar COLLATE "pg_catalog"."default",
  "state" varchar COLLATE "pg_catalog"."default",
  "event" varchar COLLATE "pg_catalog"."default",
  "affiliate_account" varchar COLLATE "pg_catalog"."default",
  "influencer_id" int4,
  "op_id" varchar COLLATE "pg_catalog"."default",
  -- "task_id" int4,
  "workflow_param_id" int4,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" timestamp(6)
)
;

-- ----------------------------
-- Records of workflows
-- ----------------------------

-- ----------------------------
-- Function structure for array_to_vector
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."array_to_vector"(_float4, int4, bool);
CREATE OR REPLACE FUNCTION "public"."array_to_vector"(_float4, int4, bool)
  RETURNS "public"."vector" AS '$libdir/vector', 'array_to_vector'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for array_to_vector
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."array_to_vector"(_numeric, int4, bool);
CREATE OR REPLACE FUNCTION "public"."array_to_vector"(_numeric, int4, bool)
  RETURNS "public"."vector" AS '$libdir/vector', 'array_to_vector'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for array_to_vector
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."array_to_vector"(_int4, int4, bool);
CREATE OR REPLACE FUNCTION "public"."array_to_vector"(_int4, int4, bool)
  RETURNS "public"."vector" AS '$libdir/vector', 'array_to_vector'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for array_to_vector
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."array_to_vector"(_float8, int4, bool);
CREATE OR REPLACE FUNCTION "public"."array_to_vector"(_float8, int4, bool)
  RETURNS "public"."vector" AS '$libdir/vector', 'array_to_vector'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for cosine_distance
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."cosine_distance"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."cosine_distance"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."float8" AS '$libdir/vector', 'cosine_distance'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for hnswhandler
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."hnswhandler"(internal);
CREATE OR REPLACE FUNCTION "public"."hnswhandler"(internal)
  RETURNS "pg_catalog"."index_am_handler" AS '$libdir/vector', 'hnswhandler'
  LANGUAGE c VOLATILE
  COST 1;

-- ----------------------------
-- Function structure for inner_product
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."inner_product"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."inner_product"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."float8" AS '$libdir/vector', 'inner_product'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for ivfflathandler
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."ivfflathandler"(internal);
CREATE OR REPLACE FUNCTION "public"."ivfflathandler"(internal)
  RETURNS "pg_catalog"."index_am_handler" AS '$libdir/vector', 'ivfflathandler'
  LANGUAGE c VOLATILE
  COST 1;

-- ----------------------------
-- Function structure for l1_distance
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."l1_distance"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."l1_distance"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."float8" AS '$libdir/vector', 'l1_distance'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for l2_distance
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."l2_distance"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."l2_distance"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."float8" AS '$libdir/vector', 'l2_distance'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for update_timestamp_column
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."update_timestamp_column"();
CREATE OR REPLACE FUNCTION "public"."update_timestamp_column"()
  RETURNS "pg_catalog"."trigger" AS $BODY$
BEGIN
NEW.update_timestamp := now();
RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-- ----------------------------
-- Function structure for vector
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector"("public"."vector", int4, bool);
CREATE OR REPLACE FUNCTION "public"."vector"("public"."vector", int4, bool)
  RETURNS "public"."vector" AS '$libdir/vector', 'vector'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_accum
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_accum"(_float8, "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_accum"(_float8, "public"."vector")
  RETURNS "pg_catalog"."_float8" AS '$libdir/vector', 'vector_accum'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_add
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_add"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_add"("public"."vector", "public"."vector")
  RETURNS "public"."vector" AS '$libdir/vector', 'vector_add'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_avg
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_avg"(_float8);
CREATE OR REPLACE FUNCTION "public"."vector_avg"(_float8)
  RETURNS "public"."vector" AS '$libdir/vector', 'vector_avg'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_cmp
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_cmp"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_cmp"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."int4" AS '$libdir/vector', 'vector_cmp'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_combine
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_combine"(_float8, _float8);
CREATE OR REPLACE FUNCTION "public"."vector_combine"(_float8, _float8)
  RETURNS "pg_catalog"."_float8" AS '$libdir/vector', 'vector_combine'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_dims
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_dims"("public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_dims"("public"."vector")
  RETURNS "pg_catalog"."int4" AS '$libdir/vector', 'vector_dims'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_eq
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_eq"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_eq"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."bool" AS '$libdir/vector', 'vector_eq'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_ge
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_ge"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_ge"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."bool" AS '$libdir/vector', 'vector_ge'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_gt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_gt"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_gt"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."bool" AS '$libdir/vector', 'vector_gt'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_in
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_in"(cstring, oid, int4);
CREATE OR REPLACE FUNCTION "public"."vector_in"(cstring, oid, int4)
  RETURNS "public"."vector" AS '$libdir/vector', 'vector_in'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_l2_squared_distance
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_l2_squared_distance"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_l2_squared_distance"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."float8" AS '$libdir/vector', 'vector_l2_squared_distance'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_le
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_le"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_le"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."bool" AS '$libdir/vector', 'vector_le'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_lt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_lt"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_lt"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."bool" AS '$libdir/vector', 'vector_lt'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_mul
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_mul"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_mul"("public"."vector", "public"."vector")
  RETURNS "public"."vector" AS '$libdir/vector', 'vector_mul'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_ne
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_ne"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_ne"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."bool" AS '$libdir/vector', 'vector_ne'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_negative_inner_product
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_negative_inner_product"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_negative_inner_product"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."float8" AS '$libdir/vector', 'vector_negative_inner_product'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_norm
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_norm"("public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_norm"("public"."vector")
  RETURNS "pg_catalog"."float8" AS '$libdir/vector', 'vector_norm'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_out
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_out"("public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_out"("public"."vector")
  RETURNS "pg_catalog"."cstring" AS '$libdir/vector', 'vector_out'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_recv
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_recv"(internal, oid, int4);
CREATE OR REPLACE FUNCTION "public"."vector_recv"(internal, oid, int4)
  RETURNS "public"."vector" AS '$libdir/vector', 'vector_recv'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_send
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_send"("public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_send"("public"."vector")
  RETURNS "pg_catalog"."bytea" AS '$libdir/vector', 'vector_send'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_spherical_distance
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_spherical_distance"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_spherical_distance"("public"."vector", "public"."vector")
  RETURNS "pg_catalog"."float8" AS '$libdir/vector', 'vector_spherical_distance'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_sub
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_sub"("public"."vector", "public"."vector");
CREATE OR REPLACE FUNCTION "public"."vector_sub"("public"."vector", "public"."vector")
  RETURNS "public"."vector" AS '$libdir/vector', 'vector_sub'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_to_float4
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_to_float4"("public"."vector", int4, bool);
CREATE OR REPLACE FUNCTION "public"."vector_to_float4"("public"."vector", int4, bool)
  RETURNS "pg_catalog"."_float4" AS '$libdir/vector', 'vector_to_float4'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for vector_typmod_in
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."vector_typmod_in"(_cstring);
CREATE OR REPLACE FUNCTION "public"."vector_typmod_in"(_cstring)
  RETURNS "pg_catalog"."int4" AS '$libdir/vector', 'vector_typmod_in'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."influencer_manual_tags_id_seq"
OWNED BY "public"."influencer_manual_tags"."id";
SELECT setval('"public"."influencer_manual_tags_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."influencer_param_histories_id_seq"
OWNED BY "public"."influencer_param_histories"."id";
SELECT setval('"public"."influencer_param_histories_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."influencers_id_seq"
OWNED BY "public"."influencers"."id";
SELECT setval('"public"."influencers_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."items_id_seq"
OWNED BY "public"."items"."id";
SELECT setval('"public"."items_id_seq"', 2, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."msg_store_id_seq"
OWNED BY "public"."msg_store"."id";
SELECT setval('"public"."msg_store_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."msg_tasks_id_seq"
OWNED BY "public"."msg_tasks"."id";
SELECT setval('"public"."msg_tasks_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."new_msgs_id_seq"
OWNED BY "public"."new_msgs"."id";
SELECT setval('"public"."new_msgs_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."system_admin_id_seq"
OWNED BY "public"."system_admin"."id";
SELECT setval('"public"."system_admin_id_seq"', 3, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."system_dept_id_seq"
OWNED BY "public"."system_dept"."id";
SELECT setval('"public"."system_dept_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."system_menu_id_seq"
OWNED BY "public"."system_menu"."id";
SELECT setval('"public"."system_menu_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."system_post_id_seq"
OWNED BY "public"."system_post"."id";
SELECT setval('"public"."system_post_id_seq"', 2, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."system_role_id_seq"
OWNED BY "public"."system_role"."id";
SELECT setval('"public"."system_role_id_seq"', 3, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."system_role_menu_id_seq"
OWNED BY "public"."system_role_menu"."id";
SELECT setval('"public"."system_role_menu_id_seq"', 49, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."upload_folder_id_seq"
OWNED BY "public"."upload_folder"."id";
SELECT setval('"public"."upload_folder_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."upload_id_seq"
OWNED BY "public"."upload"."id";
SELECT setval('"public"."upload_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."user_id_seq"
OWNED BY "public"."user"."id";
SELECT setval('"public"."user_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."workflow_params_id_seq"
OWNED BY "public"."workflow_params"."id";
SELECT setval('"public"."workflow_params_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."workflows_id_seq"
OWNED BY "public"."workflows"."id";
SELECT setval('"public"."workflows_id_seq"', 1, false);

-- ----------------------------
-- Uniques structure for table influencer_manual_tags
-- ----------------------------
ALTER TABLE "public"."influencer_manual_tags" ADD CONSTRAINT "influencer_manual_tags_influencer_id_key" UNIQUE ("influencer_id");

-- ----------------------------
-- Primary Key structure for table influencer_manual_tags
-- ----------------------------
ALTER TABLE "public"."influencer_manual_tags" ADD CONSTRAINT "influencer_manual_tags_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table influencer_param_histories
-- ----------------------------
ALTER TABLE "public"."influencer_param_histories" ADD CONSTRAINT "influencer_param_histories_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table influencers
-- ----------------------------
ALTER TABLE "public"."influencers" ADD CONSTRAINT "influencers_site_id_influencer_account_key" UNIQUE ("site_id", "influencer_account");

-- ----------------------------
-- Primary Key structure for table influencers
-- ----------------------------
ALTER TABLE "public"."influencers" ADD CONSTRAINT "influencers_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table items
-- ----------------------------
ALTER TABLE "public"."items" ADD CONSTRAINT "items_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table msg_store
-- ----------------------------
ALTER TABLE "public"."msg_store" ADD CONSTRAINT "msg_store_influencer_id_key" UNIQUE ("influencer_id");

-- ----------------------------
-- Primary Key structure for table msg_store
-- ----------------------------
ALTER TABLE "public"."msg_store" ADD CONSTRAINT "msg_store_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table msg_tasks
-- ----------------------------
ALTER TABLE "public"."msg_tasks" ADD CONSTRAINT "msg_tasks_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table new_msgs
-- ----------------------------
ALTER TABLE "public"."new_msgs" ADD CONSTRAINT "new_msgs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Triggers structure for table system_admin
-- ----------------------------
CREATE TRIGGER "system_admin" BEFORE UPDATE ON "public"."system_admin"
FOR EACH ROW
EXECUTE PROCEDURE "public"."update_timestamp_column"();

-- ----------------------------
-- Primary Key structure for table system_admin
-- ----------------------------
ALTER TABLE "public"."system_admin" ADD CONSTRAINT "system_admin_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Triggers structure for table system_dept
-- ----------------------------
CREATE TRIGGER "system_dept" BEFORE UPDATE ON "public"."system_dept"
FOR EACH ROW
EXECUTE PROCEDURE "public"."update_timestamp_column"();

-- ----------------------------
-- Primary Key structure for table system_dept
-- ----------------------------
ALTER TABLE "public"."system_dept" ADD CONSTRAINT "system_dept_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Triggers structure for table system_menu
-- ----------------------------
CREATE TRIGGER "system_menu" BEFORE UPDATE ON "public"."system_menu"
FOR EACH ROW
EXECUTE PROCEDURE "public"."update_timestamp_column"();

-- ----------------------------
-- Primary Key structure for table system_menu
-- ----------------------------
ALTER TABLE "public"."system_menu" ADD CONSTRAINT "system_menu_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table system_post
-- ----------------------------
ALTER TABLE "public"."system_post" ADD CONSTRAINT "system_post_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table system_role
-- ----------------------------
ALTER TABLE "public"."system_role" ADD CONSTRAINT "system_role_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table system_role_menu
-- ----------------------------
ALTER TABLE "public"."system_role_menu" ADD CONSTRAINT "system_role_menu_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table upload
-- ----------------------------
ALTER TABLE "public"."upload" ADD CONSTRAINT "upload_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table upload_folder
-- ----------------------------
ALTER TABLE "public"."upload_folder" ADD CONSTRAINT "upload_folder_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user
-- ----------------------------
ALTER TABLE "public"."user" ADD CONSTRAINT "user_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table workflow_params
-- ----------------------------
ALTER TABLE "public"."workflow_params" ADD CONSTRAINT "workflow_params_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table workflows
-- ----------------------------
ALTER TABLE "public"."workflows" ADD CONSTRAINT "workflows_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table influencer_manual_tags
-- ----------------------------
ALTER TABLE "public"."influencer_manual_tags" ADD CONSTRAINT "influencer_manual_tags_influencer_id_fkey" FOREIGN KEY ("influencer_id") REFERENCES "public"."influencers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table influencer_param_histories
-- ----------------------------
ALTER TABLE "public"."influencer_param_histories" ADD CONSTRAINT "influencer_param_histories_influencer_id_fkey" FOREIGN KEY ("influencer_id") REFERENCES "public"."influencers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table msg_store
-- ----------------------------
ALTER TABLE "public"."msg_store" ADD CONSTRAINT "msg_store_influencer_id_fkey" FOREIGN KEY ("influencer_id") REFERENCES "public"."influencers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table msg_tasks
-- ----------------------------
ALTER TABLE "public"."msg_tasks" ADD CONSTRAINT "msg_tasks_influencer_id_fkey" FOREIGN KEY ("influencer_id") REFERENCES "public"."influencers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."msg_tasks" ADD CONSTRAINT "msg_tasks_workflow_id_fkey" FOREIGN KEY ("workflow_id") REFERENCES "public"."workflows" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table new_msgs
-- ----------------------------
ALTER TABLE "public"."new_msgs" ADD CONSTRAINT "new_msgs_msg_store_id_fkey" FOREIGN KEY ("msg_store_id") REFERENCES "public"."msg_store" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table workflows
-- ----------------------------
ALTER TABLE "public"."workflows" ADD CONSTRAINT "workflows_influencer_id_fkey" FOREIGN KEY ("influencer_id") REFERENCES "public"."influencers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."workflows" ADD CONSTRAINT "workflows_task_id_fkey" FOREIGN KEY ("task_id") REFERENCES "public"."msg_tasks" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."workflows" ADD CONSTRAINT "workflows_workflow_param_id_fkey" FOREIGN KEY ("workflow_param_id") REFERENCES "public"."workflow_params" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
