import {Composition} from "remotion";
import {
  perspectiveGridSchema,
  TechPerspectiveGridBackground,
} from "./Composition";
import "./index.css";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="TechPerspectiveGrid2K"
      component={TechPerspectiveGridBackground}
      durationInFrames={300}
      fps={30}
      width={2560}
      height={1440}
      schema={perspectiveGridSchema}
      defaultProps={{
        backgroundColor: "#050608",
        gridColor: "#87909c",
        glowColor: "#b7d7ff",
        gridOpacity: 0.46,
        glowIntensity: 0.62,
        fogStrength: 0.72,
        gridDensity: 18,
        travelCells: 4,
        horizonRatio: 0.44,
      }}
    />
  );
};
