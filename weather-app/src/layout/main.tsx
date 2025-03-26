import { Grid, Cell } from "baseui/layout-grid";



export default function GridLayout() {
  return (
    <Grid>
      <Cell span={12}>Header</Cell>
      <Cell span={[4, 3, 2]}>Sidebar</Cell>
      <Cell span={[8, 9, 10]}>Main Content</Cell>
      <Cell span={12}>Footer</Cell>
    </Grid>
  );
}