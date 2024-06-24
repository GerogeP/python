-- 任务参数
CREATE TABLE IF NOT EXISTS workflow_params (
    id SERIAL PRIMARY KEY,
    param JSONB NOT NULL -- json格式的参数列表，包括达人账号，产品信息，达人的标签等
);


-- 达人信息
CREATE TABLE IF NOT EXISTS influencers (
    id SERIAL PRIMARY KEY,
    site_id VARCHAR, -- 站点（tiktok, ins等）
    influencer_account VARCHAR, -- 达人站内账号或 email
    -- current_workflow_id INTEGER, -- 达人当前或者上一个工作流id
    param JSONB NOT NULL, -- json 格式，存储姓名、标签等
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE (site_id, influencer_account)
);

-- 工作流实例
CREATE TABLE IF NOT EXISTS workflows (
    id SERIAL PRIMARY KEY,
    template_id VARCHAR NOT NULL, -- 工作流模板id
    state VARCHAR NOT NULL, -- 当前状态
    event VARCHAR, -- 进入这个状态的事件
    -- affiliate_account VARCHAR NOT NULL, -- BD的账号，因 TK 可能对应多个affiliate账号在管理
    affiliate_id INTEGER, -- BD的账号id，因 TK 可能对应多个affiliate账号在管理
    influencer_id INTEGER NOT NULL, -- 关联的达人信息（id）
    op_id VARCHAR NOT NULL, -- 最近一次操作这个工作流的用户，可能是系统
    -- task_id INTEGER, -- 关联的任务 id，例如消息发送任务的id
    workflow_param_id INTEGER, -- 指向下面的task_params参数表（参数包括达人 id，产品信息等）
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (workflow_param_id) REFERENCES workflow_params(id),
    FOREIGN KEY (influencer_id) REFERENCES influencers(id),
);

-- 达人 affiliate 工作流 关联表
CREATE TABLE IF NOT EXISTS influencer_affiliate_workflow (
	id SERIAL PRIMARY KEY,
	influencer_id INT,
	-- affiliate_account VARCHAR,
    affiliate_id INTEGER,
	current_workflow_id INT,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	deleted_at TIMESTAMP,
    UNIQUE ( influencer_id, affiliate_id, current_workflow_id )
);

-- 机构表
Create table affiliates
(
    id serial PRIMARY KEY,
    site_id varchar NOT NULL, -- 站点（tiktok, ins等）
    affiliate_account varchar, -- 达人站内账号或 email
    nickname varchar, -- 昵称
    home_page varchar, -- 主页
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    UNIQUE ( site_id, affiliate_account )
);


-- 发送任务
CREATE TABLE IF NOT EXISTS msg_tasks (
    id SERIAL PRIMARY KEY,
    task_type VARCHAR NOT NULL, -- 消息类型（站内消息、email）
    -- affiliate_account VARCHAR, -- BD的账号，因 TK 可能对应多个affiliate账号在管理
    affiliate_id INTEGER, -- BD的账号ID，因 TK 可能对应多个affiliate账号在管理
    influencer_id INTEGER, -- 关联的达人信息（id）
    state VARCHAR, -- 发送状态（待发送、已发送、失败）
    error_msg VARCHAR,
    msg_list JSONB, -- 待发送的消息
    workflow_id INTEGER, -- 关联的工作流实例
    workflow_event VARCHAR, -- 消息发送完成后应当触发的事件
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id),
    FOREIGN KEY (influencer_id) REFERENCES influencers(id)
);

-- ALTER TABLE workflows DROP CONSTRAINT IF EXISTS workflows_task_id_fkey;
-- ALTER TABLE workflows ADD CONSTRAINT workflows_task_id_fkey FOREIGN KEY (task_id) REFERENCES msg_tasks(id);

-- 消息列表
CREATE TABLE IF NOT EXISTS msg_store (
    id SERIAL PRIMARY KEY,
    influencer_id INTEGER UNIQUE, -- 达人账号
    msg_list JSONB NOT NULL, -- json格式的消息列表，字段有processed BOOLEAN：消息是否已经处理，Msg_type：消息类型（站内消息、email），以及时间戳等
    msg_updated_at TIMESTAMP, -- 消息更新时间
    affiliate_id INTEGER, -- BD的账号ID，因 TK 可能对应多个affiliate账号在管理
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (influencer_id) REFERENCES influencers(id)
);


CREATE TABLE IF NOT EXISTS new_msgs (
    id SERIAL PRIMARY KEY,
    msg_store_id INTEGER, -- 指向msg_store表
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (msg_store_id) REFERENCES msg_store(id)
);


-- 达人历史信息
CREATE TABLE IF NOT EXISTS influencer_param_histories (
    id SERIAL PRIMARY KEY,
    influencer_id INTEGER, -- 指向influencers表
    param JSONB NOT NULL, -- 达人的历史信息，多项历史则分多条记录
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 用这个字段记载本项历史的创建时间
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (influencer_id) REFERENCES influencers(id)
);

-- 手动加上的达人标签
CREATE TABLE IF NOT EXISTS influencer_manual_tags (
    id SERIAL PRIMARY KEY,
    influencer_id INTEGER UNIQUE, -- 指向influencers表
    tags VARCHAR(255)[] NOT NULL, -- 数组形式存储tags
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,
    FOREIGN KEY (influencer_id) REFERENCES influencers(id)
);

-- 推广任务
CREATE TABLE IF NOT EXISTS promotion_tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR, -- 任务标题
    site_id VARCHAR, -- 站点（tiktok, ins等）
    description VARCHAR, -- 描述
    product_card_id INTEGER NOT NULL, -- 关联产品
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);
--推广任务，工作流中间表
CREATE TABLE IF NOT EXISTS promotion_task_workflow (
    id SERIAL PRIMARY KEY,
		promotion_task_id INTEGER NOT NULL, -- 推广任务
    workflow_id INTEGER NOT NULL -- 关联工作流
);
