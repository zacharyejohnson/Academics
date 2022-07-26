
package csci366finalproject;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.ResultSet; 
import java.sql.Statement; 

/**
 *
 * @author Zach J; G15
 * The App class establishes a connection to postgreSQL DB to be used in Application
 */
public class App {

    private final String url = "jdbc:postgresql://localhost:5432/Computer Science Department";
    private final String user = "zacharyejohnson";
    private final String password = "Century109.iwmng";

    /**
     * Connect to the PostgreSQL database
     *
     * @return a Connection object
     */
    public Connection connect() {
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected to the PostgreSQL server successfully.");
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        return conn;
    }
    
    String query = "SELECT * FROM STUDENT"; 
  public static void viewTable(Connection con, String query) throws SQLException {
    
    try (Statement stmt = con.createStatement()) {
      ResultSet rs = stmt.executeQuery(query);
      while (rs.next()) {
        String coffeeName = rs.getString("COF_NAME");
        int supplierID = rs.getInt("SUP_ID");
        float price = rs.getFloat("PRICE");
        int sales = rs.getInt("SALES");
        int total = rs.getInt("TOTAL");
        System.out.println(coffeeName + ", " + supplierID + ", " + price +
                           ", " + sales + ", " + total);
      }
    } catch (SQLException e) {
        System.out.print(e);
    }
  }
    
    
}