import pandas as pd
import plotly_express as px
import regex as re

from levseq_dash.app import global_strings as gs


def creat_heatmap(df, plate_number, property_stat, cas_number):
    filtered_df = df[(df[gs.c_cas] == cas_number) & (df[gs.c_plate] == plate_number)]

    well_letters = filtered_df[gs.c_well].str[0]
    filtered_df["X-L"] = well_letters
    well_numbers = filtered_df[gs.c_well].str[1:].astype(int)
    filtered_df["Y-N"] = well_numbers

    heatmap_data = filtered_df.pivot(index="Y-N", columns="X-L", values=property_stat)

    annotations_data = filtered_df.pivot(index="Y-N", columns="X-L", values=gs.mutations)
    # extract = df["amino_acid_substitutions"].to_list()

    fig = px.imshow(
        heatmap_data.values,
        labels=dict(x="(A-H)", y="(1-12)", color="Values"),
        x=heatmap_data.columns,  # X-axis labels (letters A-H)
        y=heatmap_data.index,  # Y-axis labels (numbers 1-12)
        # color_continuous_scale="Viridis",
        color_continuous_scale="RdBu_r",
        # color_continuous_scale="turbo",
        aspect="auto",
        # labels={
        #     "x": "Amino acid substitutions",
        #     "y": "Position",
        #     "color": y,
        # },
        # aspect argument to "auto" will instead fill the plotting area with the heatmap, using non-square tiles
    )
    fig.update_traces(text=annotations_data, texttemplate="%{text}")
    # fig.add_annotation( x=x_label, y=y_label, text=str(annotation),  # Annotation text from column F
    # showarrow=False, font=dict(color="white" if heatmap_data.loc[y_label, x_label] < max(
    # heatmap_data.values.flatten()) / 2 else "black")

    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(len(heatmap_data.columns))),  # Tick positions
        ticktext=heatmap_data.columns,  # Custom tick labels (letters A-H)
    )
    fig.update_yaxes(
        tickmode="array",
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # list(range(len(heatmap_data.index))),  # Tick positions
        ticktext=heatmap_data.index,  # Custom tick labels (numbers 1-12, reversed)
    )

    # removing paddings
    fig.update_layout(
        margin=dict(l=0, r=0, b=0),  # Set all margins to 0
        # width=500,  # Adjust figure width
        height=600,  # Adjust figure height
        xaxis_title="",
        yaxis_title="",
    )
    fig.update_coloraxes(colorbar=dict(thickness=10, xpad=0))  # shrink the axes on the right
    # fig.update_layout(autosize=False)  # TODO: do I need this

    # # #####
    # # Create the surface plot using Plotly Express
    # filtered_df_2 = df[(df[gs.c_cas] == cas_number) & (df[gs.c_plate] == plate_number)]
    # filtered_df_2 = filtered_df_2.fillna(0)
    # selected_columns = filtered_df_2[["x_coordinate", "y_coordinate", "fitness_value"]]
    #
    # z = filtered_df.pivot(index="y_coordinate", columns="x_coordinate", values="fitness_value").values
    # #x = np.sort(df["X"].unique())
    # #y = np.sort(df["Y"].unique())
    # # fig = px.imshow(
    #     z,
    #     x="x_coordinate",
    #     y="y_coordinate",
    #     color_continuous_scale="Viridis",
    #     labels={"x": "X Coordinates", "y": "Y Coordinates", "color": "Fitness"},
    # )
    # fig.show()
    #
    # # Update layout for better aesthetics
    # fig.update_layout(
    #     title="Surface Plot of Fitness",
    #     margin=dict(l=0, r=0, t=50, b=0),
    # )
    #
    # # Customize hover template
    # fig.update_traces(
    #     hovertemplate="X: %{x}<br>Y: %{y}<br>Fitness: %{z}<extra></extra>"
    # )
    #
    # # Show the plot
    # fig.show()
    #
    #
    # # Show the plot
    # fig.show()

    #####

    return fig


def is_valid_format(s):
    return bool(re.fullmatch(r"[A-Za-z]\d+[A-Za-z]", s))

    # Helper function to extract numbers from valid strings


def extract_numbers(s):
    match = re.findall(r"\d+", s)
    return "_".join(match) if match else "NoNumbers"


def create_sunburst(df):
    # Sor on fitness
    sorted_by_fitness = df.sort_values(by="fitness_value", ascending=False)

    # Extract the top 20 rows
    top_fitness_values = sorted_by_fitness[
        ["cas_number", "plate", "well", "amino_acid_substitutions", "fitness_value"]
    ].head(200)

    # Process data to create hierarchical relationships
    processed_data = []
    # for item in data:
    for _, row in top_fitness_values.iterrows():
        item = row["amino_acid_substitutions"]
        if "#" not in item:
            components = item.split("_")
            components = [c for c in components if is_valid_format(c)]  # Keep only valid components
            n_components = len(components)  # Number of valid components in the string
            for component in components:
                numeric_part = extract_numbers(component)
                processed_data.append(
                    {
                        "Index": int(numeric_part),
                        "Group Size": f"Group-{n_components}",
                        "Combination": item,  # "_".join(components),
                        "Fitness": row["fitness_value"],
                    }
                )

    # Convert processed data to a DataFrame for sunburst and treemap charts
    df_hierarchy = pd.DataFrame(processed_data)

    group_count = df_hierarchy.groupby("Group Size")["Index"].transform("count")
    df_hierarchy["group_count"] = group_count

    df_hierarchy = df_hierarchy.sort_values(by="Index", ascending=True)
    fig_sunburst = px.sunburst(
        df_hierarchy,
        path=["Index", "Group Size", "Combination"],  # Hierarchical path
        color="Fitness",
        color_continuous_scale="RdBu",
        # values="Group Size",
        # color_discrete_map={'5': 'black', '1': 'gold'}
        # title="Hierarchical Relationships by Index (Sunburst)"
        # to use with the custom colors
        # color="Custom Color",  # Use the custom color column
    )
    fig_sunburst.show()
    fig_sunburst.update_traces(sort=False, selector=dict(type="sunburst"))

    fig_sunburst = px.sunburst(
        df_hierarchy,
        path=["Group Size", "Combination"],  # Hierarchical path
        color="Fitness",
        color_continuous_scale="RdBu",
        # color="GroupOrder",  # Use the GroupOrder to influence the display order
        # values="Group Size",
        # color_discrete_map={'5': 'black', '1': 'gold'}
        # title="Hierarchical Relationships by Index (Sunburst)"
        # to use with the custom colors
        # color="Custom Color",  # Use the custom color column
    )

    fig_sunburst.update_traces(sort=False, selector=dict(type="sunburst"))

    fig_sunburst.show()

    # Calculate the count of items for each parent category

    fig_ice = px.icicle(
        df_hierarchy,
        path=["Index", "Group Size", "Combination"],  # Hierarchical path
        # color="count",
        # color_continuous_scale="RdBu",
        color="group_count",  # Use the count of items for coloring
        color_continuous_scale="Blues",  # Customize the color scale
        # values="Group Size",
        # color_discrete_map={'5': 'black', '1': 'gold'}
        # title="Hierarchical Relationships by Index (Sunburst)"
        # to use with the custom colors
        # color="Custom Color",  # Use the custom color column
    )
    fig_ice.show()

    fig_sunburst = px.sunburst(
        df_hierarchy,
        path=["Index", "Group Size", "Combination"],  # Hierarchical path
        # color="Fitness",
        color_continuous_scale="RdBu",
        color="group_count",  # Use the count of items for coloring
        # color_continuous_scale="Blues",  # Customize the color scale
        # values="Group Size",
        # color_discrete_map={'5': 'black', '1': 'gold'}
        # title="Hierarchical Relationships by Index (Sunburst)"
        # to use with the custom colors
        # color="Custom Color",  # Use the custom color column
    )
    fig_sunburst.show()


# from levseq_dash.app.file_manager import experiment_ep_example
#
# exp = experiment_ep_example
# create_sunburst(exp.data_df)
