--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

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

--
-- Name: car_id_number; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.car_id_number AS text
	CONSTRAINT custom_domain_check CHECK ((VALUE ~ '^[1-9][0-9]{3}[A-Z]$'::text));


ALTER DOMAIN public.car_id_number OWNER TO postgres;

--
-- Name: weightkg; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.weightkg AS integer
	CONSTRAINT positive_integer_range_1_1000_check CHECK (((VALUE >= 1) AND (VALUE <= 1000)));


ALTER DOMAIN public.weightkg OWNER TO postgres;

--
-- Name: calculate_distance_miles(double precision, double precision, double precision, double precision); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.calculate_distance_miles(lat1 double precision, lon1 double precision, lat2 double precision, lon2 double precision) RETURNS double precision
    LANGUAGE plpgsql
    AS $$
DECLARE
    earth_radius FLOAT := 3959; -- Radius of the Earth in miles
    delta_lat FLOAT := RADIANS(lat2 - lat1);
    delta_lon FLOAT := RADIANS(lon2 - lon1);
    a FLOAT;
    c FLOAT;
    distance FLOAT;
BEGIN
    a := SIN(delta_lat/2) * SIN(delta_lat/2) +
         COS(RADIANS(lat1)) * COS(RADIANS(lat2)) *
         SIN(delta_lon/2) * SIN(delta_lon/2);
    c := 2 * atan2(sqrt(a), sqrt(1-a));
    distance := earth_radius * c;
    RETURN distance;
END;
$$;


ALTER FUNCTION public.calculate_distance_miles(lat1 double precision, lon1 double precision, lat2 double precision, lon2 double precision) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cargo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cargo (
    id integer NOT NULL,
    pickup_location character varying(5) NOT NULL,
    delivery_location character varying(5) NOT NULL,
    weight public.weightkg NOT NULL,
    description text
);


ALTER TABLE public.cargo OWNER TO postgres;

--
-- Name: cargo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cargo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cargo_id_seq OWNER TO postgres;

--
-- Name: cargo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cargo_id_seq OWNED BY public.cargo.id;


--
-- Name: location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location (
    zip character varying(5) NOT NULL,
    lat double precision NOT NULL,
    lng double precision NOT NULL,
    city text NOT NULL,
    state_name text NOT NULL
);


ALTER TABLE public.location OWNER TO postgres;

--
-- Name: truck; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.truck (
    number_id public.car_id_number NOT NULL,
    capacity public.weightkg NOT NULL,
    latitude double precision DEFAULT ((random() * ((49.384358 - 24.396308))::double precision) + (24.396308)::double precision),
    longitude double precision DEFAULT ((random() * (('-66.934570'::numeric - '-125.000000'::numeric))::double precision) + ('-125.000000'::numeric)::double precision)
);


ALTER TABLE public.truck OWNER TO postgres;

--
-- Name: trucks_near_cargo; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.trucks_near_cargo AS
 SELECT cargo.id AS cargo_id,
    public.calculate_distance_miles(truck.latitude, truck.longitude, location.lat, location.lng) AS distance,
    truck.number_id
   FROM public.truck,
    (public.cargo
     LEFT JOIN public.location ON (((cargo.pickup_location)::text = (location.zip)::text)));


ALTER TABLE public.trucks_near_cargo OWNER TO postgres;

--
-- Name: cargo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargo ALTER COLUMN id SET DEFAULT nextval('public.cargo_id_seq'::regclass);


--
-- Data for Name: cargo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cargo (id, pickup_location, delivery_location, weight, description) FROM stdin;
\.


--
-- Data for Name: location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location (zip, lat, lng, city, state_name) FROM stdin;
\.


--
-- Data for Name: truck; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.truck (number_id, capacity, latitude, longitude) FROM stdin;
2345H	1000	36.30527901427006	-110.57099809581766
5555H	1000	30.444581717532724	-111.1961407496103
1000H	500	45.2020309856924	-99.35216352248818
1123H	500	42.9023061505465	-98.09021100624962
1124H	500	39.43176277594637	-103.40932062751652
6424H	500	44.03400089046409	-75.71904376207598
7392H	500	44.011021412521934	-78.46538177428786
2370H	500	47.68845937725604	-69.67319484037117
2222H	500	43.597202393837385	-102.84511430796613
8203H	500	34.74593286393966	-79.9003014764724
2783L	500	32.35980917191707	-107.35159688372838
7893L	500	47.98436822022849	-115.06424111112769
2383L	500	44.17895247478397	-86.03494155317169
8290L	500	40.451654504432945	-94.31630399151081
8290R	500	35.66116950625789	-95.29892140998632
7839R	500	36.647146411991855	-95.43014044626858
3728R	500	27.58664966975983	-97.04889513969006
1027R	500	30.781358703396485	-89.05008649757418
3820R	500	32.01365689074859	-124.68538810213569
6666R	1000	28.701156929627388	-105.32699985132969
\.


--
-- Name: cargo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cargo_id_seq', 1, false);


--
-- Name: cargo cargo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargo
    ADD CONSTRAINT cargo_pkey PRIMARY KEY (id);


--
-- Name: location location_zip_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_zip_key UNIQUE (zip);


--
-- Name: truck truck_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.truck
    ADD CONSTRAINT truck_pkey PRIMARY KEY (number_id);


--
-- Name: idx_zip_exact_match; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_zip_exact_match ON public.location USING btree (zip);


--
-- Name: cargo cargo_delivery_location_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargo
    ADD CONSTRAINT cargo_delivery_location_fkey FOREIGN KEY (delivery_location) REFERENCES public.location(zip);


--
-- Name: cargo cargo_pickup_location_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cargo
    ADD CONSTRAINT cargo_pickup_location_fkey FOREIGN KEY (pickup_location) REFERENCES public.location(zip);


--
-- PostgreSQL database dump complete
--

