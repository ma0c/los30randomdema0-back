CREATE DATABASE los30randomdema0;

CREATE USER los30randomdema0_user WITH PASSWORD '<secret_password>';
ALTER DATABASE los30randomdema0 OWNER TO los30randomdema0_user;
GRANT ALL PRIVILEGES ON DATABASE los30randomdema0 TO los30randomdema0_user;