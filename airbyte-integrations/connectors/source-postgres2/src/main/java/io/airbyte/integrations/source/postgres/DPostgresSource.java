package io.airbyte.integrations.source.postgres;

import static java.lang.Thread.sleep;

import io.debezium.config.Configuration;
import io.debezium.engine.ChangeEvent;
import io.debezium.engine.DebeziumEngine;
import io.debezium.engine.format.Json;
import java.io.IOException;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import org.apache.log4j.Level;
import org.apache.log4j.LogManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DPostgresSource {
  private static final Logger LOGGER = LoggerFactory.getLogger(DPostgresSource.class);

  public static void main(String[] args) throws IOException, InterruptedException {

    // Define the configuration for the Debezium Engine with MySQL connector...
//    final Properties props = config.asProperties();
    final Properties props = new Properties();
    props.setProperty("name", "engine");
    props.setProperty("plugin.name", "pgoutput");
    props.setProperty("connector.class", "io.debezium.connector.postgresql.PostgresConnector");
    props.setProperty("offset.storage", "org.apache.kafka.connect.storage.FileOffsetBackingStore");
    props.setProperty("offset.storage.file.filename", "/tmp/offsets2.dat");
    props.setProperty("offset.flush.interval.ms", "60000");
    /* begin connector properties */
//        .with("database.server.name", "orders")
//        .with("database.hostname", "localhost")
//        .with("database.port", 5432)
//        .with("database.user", "postgres")
//        .with("database.password", "postgres")
//        .with("database.dbname", "demo")
//        .with("table.whitelist", "public.orders")

    // https://debezium.io/documentation/reference/configuration/avro.html
    props.setProperty("key.converter.schemas.enable", "false");
    props.setProperty("value.converter.schemas.enable", "false");

    // https://debezium.io/documentation/reference/configuration/event-flattening.html
    props.setProperty("delete.handling.mode", "rewrite");
    props.setProperty("drop.tombstones", "false");
    props.setProperty("transforms.unwrap.type", "io.debezium.transforms.ExtractNewRecordState");

    props.setProperty("table.include.list", "public.*");
    props.setProperty("name", "orders-postgres-connector");
    props.setProperty("include_schema_changes", "true");
    props.setProperty("database.server.name", "orders");
    props.setProperty("database.hostname", "localhost");
    props.setProperty("database.port", "5432");
    props.setProperty("database.user", "postgres");
    props.setProperty("database.password", "");
    props.setProperty("database.dbname", "debezium_test");
    props.setProperty("database.history", "io.debezium.relational.history.FileDatabaseHistory"); // todo: any reason not to use in memory version and reload from
    props.setProperty("database.history.file.filename", "/tmp/debezium/dbhistory.dat");

    props.setProperty("slot.name", "debezium");

    // can set value.converter.schemas.enabled to false if we want to save space/effort for records

    // https://debezium.io/documentation/reference/1.0/connectors/postgresql.html#discrepance-between-plugins

    // https://debezium.io/blog/2020/02/25/lessons-learned-running-debezium-with-postgresql-on-rds/


// Create the engine with this configuration ...
    try (DebeziumEngine<ChangeEvent<String, String>> engine = DebeziumEngine.create(Json.class)
        .using(props)
        .notifying(record -> {
          LOGGER.info(record.toString());
        }).build()
    ) {
      // Run the engine asynchronously ...
      ExecutorService executor = Executors.newSingleThreadExecutor();
      executor.execute(engine);

      while(true) {
        sleep(5000);
//        LOGGER.info("the mummy wakes");
      }

      // Do something else or wait for a signal or an event
    }
// Engine is stopped when the main code is finished
  }

}
