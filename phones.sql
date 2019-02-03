BEGIN;
CREATE TABLE "phone_brand" ("id" serial NOT NULL PRIMARY KEY, "name" varchar(255) NOT NULL UNIQUE, "slug" varchar(50) NOT NULL, "created" timestamp with time zone NOT NULL, "updated" timestamp with time zone NOT NULL);
CREATE TABLE "phone_model" ("id" serial NOT NULL PRIMARY KEY, "name" varchar(255) NOT NULL UNIQUE, "slug" varchar(50) NOT NULL, "created" timestamp with time zone NOT NULL, "updated" timestamp with time zone NOT NULL, "brand_id" integer NOT NULL);
CREATE TABLE "phone_picture" ("id" serial NOT NULL PRIMARY KEY, "picture" varchar(100) NOT NULL, "brand_id" integer NOT NULL, "model_id" integer NOT NULL);
CREATE INDEX "phone_brand_2dbcba41" ON "phone_brand" ("slug");
CREATE INDEX "phone_brand_name_254d5d7e99ee1fdd_like" ON "phone_brand" ("name" varchar_pattern_ops);
CREATE INDEX "phone_brand_slug_58a7122cb93cb21b_like" ON "phone_brand" ("slug" varchar_pattern_ops);
ALTER TABLE "phone_model" ADD CONSTRAINT "phone_model_brand_id_4a197f17ce6881d3_fk_phone_brand_id" FOREIGN KEY ("brand_id") REFERENCES "phone_brand" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "phone_model_2dbcba41" ON "phone_model" ("slug");
CREATE INDEX "phone_model_521b20f5" ON "phone_model" ("brand_id");
CREATE INDEX "phone_model_name_1291e51c79703731_like" ON "phone_model" ("name" varchar_pattern_ops);
CREATE INDEX "phone_model_slug_4c3761e327acad07_like" ON "phone_model" ("slug" varchar_pattern_ops);
ALTER TABLE "phone_picture" ADD CONSTRAINT "phone_picture_brand_id_2257dfbd068fa5ce_fk_phone_brand_id" FOREIGN KEY ("brand_id") REFERENCES "phone_brand" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "phone_picture" ADD CONSTRAINT "phone_picture_model_id_22f69aedfeec555e_fk_phone_model_id" FOREIGN KEY ("model_id") REFERENCES "phone_model" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "phone_picture_521b20f5" ON "phone_picture" ("brand_id");
CREATE INDEX "phone_picture_477cbf8a" ON "phone_picture" ("model_id");

COMMIT;
