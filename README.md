#Create DB table in pgadmin

Use:

-- Table: public.product

-- DROP TABLE IF EXISTS public.product;

CREATE TABLE IF NOT EXISTS public.product
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 10000000 CACHE 1 ),
    product_name text COLLATE pg_catalog."default",
    product_sku text COLLATE pg_catalog."default",
    brand text COLLATE pg_catalog."default",
    quantity integer,
    CONSTRAINT product_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.product
    OWNER to openpg;
