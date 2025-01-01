--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2025-01-01 22:16:12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 227 (class 1259 OID 17148)
-- Name: benefitwisata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.benefitwisata (
    id bigint NOT NULL,
    id_benefit character varying(10),
    benefit text
);


ALTER TABLE public.benefitwisata OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 17147)
-- Name: benefitwisata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.benefitwisata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.benefitwisata_id_seq OWNER TO postgres;

--
-- TOC entry 4920 (class 0 OID 0)
-- Dependencies: 226
-- Name: benefitwisata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.benefitwisata_id_seq OWNED BY public.benefitwisata.id;


--
-- TOC entry 218 (class 1259 OID 17039)
-- Name: bis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bis (
    id_bis character varying(10) NOT NULL,
    nama_bis character varying(50),
    id_kelas_bis character varying(50),
    jasa_travel character varying(50),
    id_rute character varying(10),
    logojasatravel text,
    gbrbis text
);


ALTER TABLE public.bis OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 17084)
-- Name: detailTransaksi; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."detailTransaksi" (
    num_increment integer NOT NULL,
    id_trans character varying(10),
    id_bis character varying(10),
    tgl_pergi date,
    tgl_balik date,
    jlh_penumpang integer,
    hrg_tiket_perorg double precision
);


ALTER TABLE public."detailTransaksi" OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17083)
-- Name: detailTransaksi_num_increment_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."detailTransaksi_num_increment_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."detailTransaksi_num_increment_seq" OWNER TO postgres;

--
-- TOC entry 4921 (class 0 OID 0)
-- Dependencies: 223
-- Name: detailTransaksi_num_increment_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."detailTransaksi_num_increment_seq" OWNED BY public."detailTransaksi".num_increment;


--
-- TOC entry 219 (class 1259 OID 17044)
-- Name: kelas_bis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kelas_bis (
    id_kelas character varying(10) NOT NULL,
    nama_kelas character varying(50),
    harga double precision
);


ALTER TABLE public.kelas_bis OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 17049)
-- Name: kota; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kota (
    id_kota character varying(10) NOT NULL,
    nama_kota character varying(60)
);


ALTER TABLE public.kota OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17134)
-- Name: paketwisata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paketwisata (
    id_paket character varying(10) NOT NULL,
    nama_paket character varying(100),
    harga_paket double precision,
    id_bis character varying(10),
    rute_awal character varying(50),
    rute_akhir character varying(50),
    tgl_brkt date,
    tgl_balik date,
    id_benefit character varying(50),
    gbrpaket text,
    subjudulpaket text,
    jlhpenumpang integer,
    jambrkt time without time zone,
    jambalik time without time zone
);


ALTER TABLE public.paketwisata OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17066)
-- Name: rute; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rute (
    id character varying(10) NOT NULL,
    kota_awal character varying(30),
    kota_akhir character varying(30),
    lama_tempuh_jam character varying(30),
    waktu_berangkat character varying(10),
    waktu_sampai character varying(10)
);


ALTER TABLE public.rute OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17065)
-- Name: rute_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rute_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rute_id_seq OWNER TO postgres;

--
-- TOC entry 4922 (class 0 OID 0)
-- Dependencies: 221
-- Name: rute_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rute_id_seq OWNED BY public.rute.id;


--
-- TOC entry 228 (class 1259 OID 25522)
-- Name: stok_tiket; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stok_tiket (
    id_bis character varying(10) NOT NULL,
    total_tiket integer NOT NULL,
    tiket_tersedia integer NOT NULL
);


ALTER TABLE public.stok_tiket OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17021)
-- Name: transaksi; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaksi (
    id_trans character varying(100) NOT NULL,
    bukti_foto text,
    tgl_trans timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    email_cust text,
    id_staff character varying(10),
    status_trans character varying(50),
    total_harga double precision,
    metode_byr character varying(10),
    id_paket character varying(10),
    alasan_tolak text,
    generated_ticket character varying(10),
    user_bayar double precision,
    kembalian double precision
);


ALTER TABLE public.transaksi OWNER TO postgres;

--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 217
-- Name: COLUMN transaksi.id_paket; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.transaksi.id_paket IS 'jikalau pesan lewat paket';


--
-- TOC entry 216 (class 1259 OID 17010)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    username character varying(50),
    email character varying(100),
    passwd character varying(100),
    profile_picture text,
    no_hp bigint,
    tanggal_lahir timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    jk boolean,
    roles character varying(10) DEFAULT 'USER'::character varying,
    created_at date DEFAULT now(),
    id_staff character varying(10)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 17009)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4924 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4734 (class 2604 OID 17151)
-- Name: benefitwisata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.benefitwisata ALTER COLUMN id SET DEFAULT nextval('public.benefitwisata_id_seq'::regclass);


--
-- TOC entry 4733 (class 2604 OID 17087)
-- Name: detailTransaksi num_increment; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."detailTransaksi" ALTER COLUMN num_increment SET DEFAULT nextval('public."detailTransaksi_num_increment_seq"'::regclass);


--
-- TOC entry 4732 (class 2604 OID 17076)
-- Name: rute id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rute ALTER COLUMN id SET DEFAULT nextval('public.rute_id_seq'::regclass);


--
-- TOC entry 4727 (class 2604 OID 17013)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4913 (class 0 OID 17148)
-- Dependencies: 227
-- Data for Name: benefitwisata; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (5, 'BF002', 'Arung Jeram');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (6, 'BF002', 'Air Mancur');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (7, 'BF002', 'Pantai Kapuk');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (8, 'BF003', 'Free Mess 1 Malam');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (9, 'BF003', 'Free Makan 3x Sehari');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (10, 'BF003', 'Free Mandi');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (46, 'BF001', 'Pantai Kijing');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (47, 'BF001', 'Vihara Kulor');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (48, 'BF001', 'Batu Belimbing');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (49, 'BF001', 'MimiLand');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (16, 'BF005', 'Free Makan 3x Sehari');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (18, 'BF005', 'Yud');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (30, 'BF006', 'Arung Jeram');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (31, 'BF006', 'Binatang Kubu');
INSERT INTO public.benefitwisata (id, id_benefit, benefit) VALUES (32, 'BF006', 'ayam');


--
-- TOC entry 4904 (class 0 OID 17039)
-- Dependencies: 218
-- Data for Name: bis; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.bis (id_bis, nama_bis, id_kelas_bis, jasa_travel, id_rute, logojasatravel, gbrbis) VALUES ('DAMRI02', 'DAMRI SKW', 'EXE01', 'DAMRI', 'SKWPTK', NULL, '["0e07b6dc-e727-49f6-b5d6-1118c0586853.jpg", "fd14bd99-ad5c-4944-976e-c560130e5e96.jpg", "e673be2f-f793-439b-b292-05f045875131.jpg"]');
INSERT INTO public.bis (id_bis, nama_bis, id_kelas_bis, jasa_travel, id_rute, logojasatravel, gbrbis) VALUES ('DMRKTPPTK', 'DAMRI KETAPANG', 'EXEPTKKTP', 'DAMRI', 'KTPPTK', 'b06a1819-d0e6-44e5-bbcd-a0cc3884e285.jpg', '[]');
INSERT INTO public.bis (id_bis, nama_bis, id_kelas_bis, jasa_travel, id_rute, logojasatravel, gbrbis) VALUES ('DAMRI03', 'DAMRI KTPG', 'EXEPTKKTP', 'DAMRI', 'PTKKTP', 'ed6056f9-b71f-4918-8f25-64e7fea1df43.jpg', NULL);
INSERT INTO public.bis (id_bis, nama_bis, id_kelas_bis, jasa_travel, id_rute, logojasatravel, gbrbis) VALUES ('ATS01', 'ATS EXECUTIVEE', 'ATSEXE', 'ATS', 'PTKSKW', 'c4f17fbb-b0c3-4242-9305-91f2d6e8e0ed.jpg', NULL);
INSERT INTO public.bis (id_bis, nama_bis, id_kelas_bis, jasa_travel, id_rute, logojasatravel, gbrbis) VALUES ('ATSPTKJGP', 'ATS EXECUTIVE JGP', 'EXE01', 'ATS', 'PTKJGP', '0002eae8-edb3-4afb-8260-a2ac051ce7af.jpg', '[]');
INSERT INTO public.bis (id_bis, nama_bis, id_kelas_bis, jasa_travel, id_rute, logojasatravel, gbrbis) VALUES ('DAMRI01', 'DAMRI EXECUTIVE', 'EXE01', 'DAMRI', 'PTKSKW', '44ea9758-696c-4316-b3f8-9a6dcffa4091.jpg', '["976bb4c1-6fe2-493e-9c55-631c81ebfb6c.jpg", "5f94f001-ea62-4163-9c59-9ccade4a07ec.jpg", "87410856-fba9-4f2c-a2b0-ed493b04b673.jpg"]');
INSERT INTO public.bis (id_bis, nama_bis, id_kelas_bis, jasa_travel, id_rute, logojasatravel, gbrbis) VALUES ('ATSEXEJGP', 'ATS EXECUTIVE JGP', 'ATSEXE', 'ATS', 'JGPPTK', '41e27e53-f50e-4d05-8bd5-07ccaad595e8.jpg', '["f49a3501-48b7-447f-bea4-8f7788f57e75.jpg", "7188e8a7-0cdd-4100-a989-9aa3f2d42ee3.jpg", "25a4e2f7-2102-4efa-bfad-78add1616a68.jpg"]');
INSERT INTO public.bis (id_bis, nama_bis, id_kelas_bis, jasa_travel, id_rute, logojasatravel, gbrbis) VALUES ('ATSSBS', 'ATS EXECUTIVE SBS', 'ATSEXE', 'ATS', 'PTKSBS', '7cdfbcf7-c374-4888-afff-df39a82d210c.jpg', '[]');


--
-- TOC entry 4910 (class 0 OID 17084)
-- Dependencies: 224
-- Data for Name: detailTransaksi; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."detailTransaksi" (num_increment, id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg) VALUES (1, 'A0001', 'DAMRI01', '2024-11-30', '2024-12-01', 3, 166666.66666666666);
INSERT INTO public."detailTransaksi" (num_increment, id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg) VALUES (2, 'A0002', 'DAMRI03', '2024-11-28', '2024-11-28', 6, 420000);
INSERT INTO public."detailTransaksi" (num_increment, id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg) VALUES (6, 'A0003', 'ATSSBS', '2024-12-01', '2024-12-09', 3, 870000);
INSERT INTO public."detailTransaksi" (num_increment, id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg) VALUES (7, 'A0004', 'DAMRI03', '2024-12-02', '2024-12-02', 3, 420000);
INSERT INTO public."detailTransaksi" (num_increment, id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg) VALUES (8, 'A0005', 'DAMRI01', '2024-11-30', '2024-12-01', 3, 166666.66666666666);
INSERT INTO public."detailTransaksi" (num_increment, id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg) VALUES (9, 'A0006', 'ATS01', '2024-12-02', '2024-12-04', 5, 300000);


--
-- TOC entry 4905 (class 0 OID 17044)
-- Dependencies: 219
-- Data for Name: kelas_bis; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.kelas_bis (id_kelas, nama_kelas, harga) VALUES ('ECO02', 'Economy2', 280000);
INSERT INTO public.kelas_bis (id_kelas, nama_kelas, harga) VALUES ('EXE01', 'EXECUTIVE', 380000);
INSERT INTO public.kelas_bis (id_kelas, nama_kelas, harga) VALUES ('EXEPTKKTP', 'EXECUTIVE KTPG', 420000);
INSERT INTO public.kelas_bis (id_kelas, nama_kelas, harga) VALUES ('ATSEXE', 'EXECUTIVE BY ATS', 435000);


--
-- TOC entry 4906 (class 0 OID 17049)
-- Dependencies: 220
-- Data for Name: kota; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.kota (id_kota, nama_kota) VALUES ('PTK', 'PONTIANAK');
INSERT INTO public.kota (id_kota, nama_kota) VALUES ('SKW', 'SINGKAWANG');
INSERT INTO public.kota (id_kota, nama_kota) VALUES ('SBS', 'SAMBAS');
INSERT INTO public.kota (id_kota, nama_kota) VALUES ('JGB', 'JAGOI');


--
-- TOC entry 4911 (class 0 OID 17134)
-- Dependencies: 225
-- Data for Name: paketwisata; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.paketwisata (id_paket, nama_paket, harga_paket, id_bis, rute_awal, rute_akhir, tgl_brkt, tgl_balik, id_benefit, gbrpaket, subjudulpaket, jlhpenumpang, jambrkt, jambalik) VALUES ('P0002', 'Paket Wisata Ketapang', 1500000, 'ATS01', 'PONTIANAK', 'KETAPANG', '2024-12-02', '2024-12-04', 'BF002', '9f2883b2-eae8-4114-b50c-1ac29809110b.jpg', 'Paket Tidur 2 Hari 1 Malam', 5, '08:00:00', '13:00:00');
INSERT INTO public.paketwisata (id_paket, nama_paket, harga_paket, id_bis, rute_awal, rute_akhir, tgl_brkt, tgl_balik, id_benefit, gbrpaket, subjudulpaket, jlhpenumpang, jambrkt, jambalik) VALUES ('P0001', 'Paket Wisata Singkawang', 500000, 'DAMRI01', 'PONTIANAK', 'SINGKAWANG', '2024-11-30', '2024-12-01', 'BF001', 'bf414487-2238-44a9-92b2-85d948dbc870.jpg', 'Perjalanan 2 Hari 1 Malam', 3, '12:00:00', '16:00:00');


--
-- TOC entry 4908 (class 0 OID 17066)
-- Dependencies: 222
-- Data for Name: rute; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.rute (id, kota_awal, kota_akhir, lama_tempuh_jam, waktu_berangkat, waktu_sampai) VALUES ('PTKSKW', 'PONTIANAK', 'SINGKAWANG', '3 jam', '17:00', '20:00');
INSERT INTO public.rute (id, kota_awal, kota_akhir, lama_tempuh_jam, waktu_berangkat, waktu_sampai) VALUES ('SKWPTK', 'SINGKAWANG', 'PONTIANAK', '3 Jam', '03:00', '06:00');
INSERT INTO public.rute (id, kota_awal, kota_akhir, lama_tempuh_jam, waktu_berangkat, waktu_sampai) VALUES ('PTKSBS', 'PONTIANAK', 'SAMBAS', '5 Jam', '09:00', '14:00');
INSERT INTO public.rute (id, kota_awal, kota_akhir, lama_tempuh_jam, waktu_berangkat, waktu_sampai) VALUES ('PTKKTP', 'PONTIANAK', 'KETAPANG', '5 Jam', '15:00', '20:00');
INSERT INTO public.rute (id, kota_awal, kota_akhir, lama_tempuh_jam, waktu_berangkat, waktu_sampai) VALUES ('PTKJGP', 'PONTIANAK', 'JAGOI BABANG', '3 Jam', '19:00', '22:00');
INSERT INTO public.rute (id, kota_awal, kota_akhir, lama_tempuh_jam, waktu_berangkat, waktu_sampai) VALUES ('KTPPTK', 'KETAPANG', 'PONTIANAK', '5 Jam', '18:00', '23:00');
INSERT INTO public.rute (id, kota_awal, kota_akhir, lama_tempuh_jam, waktu_berangkat, waktu_sampai) VALUES ('JGPPTK', 'JAGOI BABANG', 'PONTIANAK', '3 Jam', '06:00', '09:00');


--
-- TOC entry 4914 (class 0 OID 25522)
-- Dependencies: 228
-- Data for Name: stok_tiket; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.stok_tiket (id_bis, total_tiket, tiket_tersedia) VALUES ('DAMRI02', 50, 50);
INSERT INTO public.stok_tiket (id_bis, total_tiket, tiket_tersedia) VALUES ('ATSSBS', 45, 45);
INSERT INTO public.stok_tiket (id_bis, total_tiket, tiket_tersedia) VALUES ('DAMRI03', 48, 39);
INSERT INTO public.stok_tiket (id_bis, total_tiket, tiket_tersedia) VALUES ('DAMRI01', 40, 34);
INSERT INTO public.stok_tiket (id_bis, total_tiket, tiket_tersedia) VALUES ('ATS01', 40, 40);
INSERT INTO public.stok_tiket (id_bis, total_tiket, tiket_tersedia) VALUES ('ATSEXEJGP', 40, 40);
INSERT INTO public.stok_tiket (id_bis, total_tiket, tiket_tersedia) VALUES ('ATSPTKJGP', 40, 40);
INSERT INTO public.stok_tiket (id_bis, total_tiket, tiket_tersedia) VALUES ('DMRKTPPTK', 40, 40);


--
-- TOC entry 4903 (class 0 OID 17021)
-- Dependencies: 217
-- Data for Name: transaksi; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.transaksi (id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr, id_paket, alasan_tolak, generated_ticket, user_bayar, kembalian) VALUES ('A0002', 'nofoto', '2024-11-28 22:20:39.659228+07', 'user2@gmail.com', 'KSR_01', 'COMPLETED', 2520000, 'cash', '', NULL, 'T-0383', 2600000, 80000);
INSERT INTO public.transaksi (id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr, id_paket, alasan_tolak, generated_ticket, user_bayar, kembalian) VALUES ('A0001', '91c6f01e-b30e-457a-9df7-40b532e5c348.jpg', '2024-11-28 22:20:08.224579+07', 'user2@gmail.com', 'ADM_01', 'COMPLETED', 500000, 'transfer', 'P0001', NULL, 'T-0006', 500000, 0);
INSERT INTO public.transaksi (id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr, id_paket, alasan_tolak, generated_ticket, user_bayar, kembalian) VALUES ('A0003', 'nofoto', '2024-12-01 22:42:48.427152+07', 'user2@gmail.com', 'ADM_01', 'CANCELLED', 2610000, 'cash', '', 'User Meminta Cancel', NULL, 0, 0);
INSERT INTO public.transaksi (id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr, id_paket, alasan_tolak, generated_ticket, user_bayar, kembalian) VALUES ('A0004', '2245b838-ef4e-4381-9af6-586a4e35ed9d.jpg', '2024-12-02 16:59:21.012986+07', 'rio@gmail.com', 'KSR_01', 'COMPLETED', 1260000, 'transfer', '', NULL, 'T-0427', 1260000, 0);
INSERT INTO public.transaksi (id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr, id_paket, alasan_tolak, generated_ticket, user_bayar, kembalian) VALUES ('A0005', 'nofoto', '2024-12-02 17:00:42.295486+07', 'rio@gmail.com', 'KSR_01', 'COMPLETED', 500000, 'cash', 'P0001', NULL, 'T-0946', 600000, 100000);
INSERT INTO public.transaksi (id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr, id_paket, alasan_tolak, generated_ticket, user_bayar, kembalian) VALUES ('A0006', 'nofoto', '2024-12-02 17:07:31.100684+07', 'rio@gmail.com', 'ADM_01', 'CANCELLED', 1500000, 'cash', 'P0002', 'tidak jadi', NULL, 0, 0);


--
-- TOC entry 4902 (class 0 OID 17010)
-- Dependencies: 216
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users (id, username, email, passwd, profile_picture, no_hp, tanggal_lahir, jk, roles, created_at, id_staff) VALUES (3, 'admin', 'admin@gmail.com', '00000000', 'nofoto', 818181, '2024-10-23 13:53:33.600832', true, 'ADMIN', '2024-10-01', 'ADM_01');
INSERT INTO public.users (id, username, email, passwd, profile_picture, no_hp, tanggal_lahir, jk, roles, created_at, id_staff) VALUES (11, 'kasir', 'kasir@gmail.com', '123', NULL, NULL, '2024-11-21 23:23:38.344691', NULL, 'KASIR', '2024-11-21', 'KSR_01');
INSERT INTO public.users (id, username, email, passwd, profile_picture, no_hp, tanggal_lahir, jk, roles, created_at, id_staff) VALUES (9, 'user1', 'user1@gmail.com', '123', '5f368544-bab7-4476-b367-39947bb3eb14.png', 12124, '2024-11-19 00:00:00', true, 'USER', '2024-11-09', NULL);
INSERT INTO public.users (id, username, email, passwd, profile_picture, no_hp, tanggal_lahir, jk, roles, created_at, id_staff) VALUES (13, 'rio', 'rio@gmail.com', '123', NULL, NULL, '2024-11-25 16:52:47.426402', NULL, 'USER', '2024-11-25', NULL);
INSERT INTO public.users (id, username, email, passwd, profile_picture, no_hp, tanggal_lahir, jk, roles, created_at, id_staff) VALUES (14, 'user2', 'user2@gmail.com', '123', 'b75a36bf-fd95-4dd7-9e9e-d7cdadcd1a3e.png', 616162, '2024-11-26 00:00:00', true, 'USER', '2024-11-25', NULL);
INSERT INTO public.users (id, username, email, passwd, profile_picture, no_hp, tanggal_lahir, jk, roles, created_at, id_staff) VALUES (15, 'stif', 'stif@gmail.com', '123', NULL, NULL, '2024-12-11 15:50:33.355728', NULL, 'USER', '2024-12-11', NULL);


--
-- TOC entry 4925 (class 0 OID 0)
-- Dependencies: 226
-- Name: benefitwisata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.benefitwisata_id_seq', 49, true);


--
-- TOC entry 4926 (class 0 OID 0)
-- Dependencies: 223
-- Name: detailTransaksi_num_increment_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."detailTransaksi_num_increment_seq"', 9, true);


--
-- TOC entry 4927 (class 0 OID 0)
-- Dependencies: 221
-- Name: rute_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rute_id_seq', 2, true);


--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 15, true);


--
-- TOC entry 4754 (class 2606 OID 17155)
-- Name: benefitwisata benefitwisata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.benefitwisata
    ADD CONSTRAINT benefitwisata_pkey PRIMARY KEY (id);


--
-- TOC entry 4742 (class 2606 OID 17043)
-- Name: bis bis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bis
    ADD CONSTRAINT bis_pkey PRIMARY KEY (id_bis);


--
-- TOC entry 4750 (class 2606 OID 17089)
-- Name: detailTransaksi detailTransaksi_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."detailTransaksi"
    ADD CONSTRAINT "detailTransaksi_pkey" PRIMARY KEY (num_increment);


--
-- TOC entry 4744 (class 2606 OID 17048)
-- Name: kelas_bis kelas_bis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kelas_bis
    ADD CONSTRAINT kelas_bis_pkey PRIMARY KEY (id_kelas);


--
-- TOC entry 4746 (class 2606 OID 17053)
-- Name: kota kota_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kota
    ADD CONSTRAINT kota_pkey PRIMARY KEY (id_kota);


--
-- TOC entry 4752 (class 2606 OID 17138)
-- Name: paketwisata paketwisata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paketwisata
    ADD CONSTRAINT paketwisata_pkey PRIMARY KEY (id_paket);


--
-- TOC entry 4748 (class 2606 OID 17078)
-- Name: rute rute_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rute
    ADD CONSTRAINT rute_pkey PRIMARY KEY (id);


--
-- TOC entry 4756 (class 2606 OID 25526)
-- Name: stok_tiket ticket_stock_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stok_tiket
    ADD CONSTRAINT ticket_stock_pkey PRIMARY KEY (id_bis);


--
-- TOC entry 4740 (class 2606 OID 17027)
-- Name: transaksi transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaksi
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id_trans);


--
-- TOC entry 4736 (class 2606 OID 17020)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4738 (class 2606 OID 17018)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4757 (class 2606 OID 25527)
-- Name: stok_tiket fk_bis; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stok_tiket
    ADD CONSTRAINT fk_bis FOREIGN KEY (id_bis) REFERENCES public.bis(id_bis) ON DELETE CASCADE;


-- Completed on 2025-01-01 22:16:12

--
-- PostgreSQL database dump complete
--

