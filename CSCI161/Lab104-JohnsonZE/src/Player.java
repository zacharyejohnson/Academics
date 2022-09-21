
import java.util.Objects;


/**
 * The player class describes player objects representing players of a game 
 * @author Zach Johnson
 * @version 9/24/2021
 */
public class Player {

    // instance variables 
    private String name; 
    private String positionPlayed; 
    private int jerseyNumber; 
    //default
    public Player(){
    }
    
    //loaded
    public Player( String playerName, String position, int jersey ){
        name = playerName; 
        positionPlayed = position; 
        jerseyNumber = jersey; 
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setPositionPlayed(String positionPlayed) {
        this.positionPlayed = positionPlayed;
    }

    public void setJerseyNumber(int jerseyNumber) {
        this.jerseyNumber = jerseyNumber;
    }

    public String getName() {
        return name;
    }

    public String getPositionPlayed() {
        return positionPlayed;
    }

    public int getJerseyNumber() {
        return jerseyNumber;
    }

    @Override
    public String toString() {
        return "Player{" + "name=" + name + ", positionPlayed=" + positionPlayed + ", jerseyNumber=" + jerseyNumber + '}';
    }
    
     @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Player other = (Player) obj;
        if (this.jerseyNumber != other.jerseyNumber) {
            return false;
        }
        if (!Objects.equals(this.name, other.name)) {
            return false;
        }
        if (!Objects.equals(this.positionPlayed, other.positionPlayed)) {
            return false;
        }
        return true;
    }
}
